import numpy as np
from django.conf import settings

from apps.history import models as history_models
from apps.first import models
from apps.history.services.similar import Similar, get_mean_and_sd
from currency.utils import get_working_bars


def worker_order():
    setting = models.Setting.objects.get(name="c90")
    for strategy in models.Strategy.objects.filter(setting=setting):
        currency = strategy.currency
        data_time = settings.START_DATE
        query_set = history_models.TimeMarker.objects.filter(time_marker__gte=data_time)
        query_set = query_set.exclude(time_marker__in=models.Order.objects.filter(strategy=strategy).values("time_marker__time_marker"))

        for time_marker in query_set.iterator():
            print(time_marker)
            root_bar = history_models.Bar.objects.get(time_marker=time_marker, currency=currency)
            similars = list(Similar.get_similar_items(
                root_bar=root_bar, n=setting.n, history_size=setting.history_size, abs_correlation=setting.abs_correlation))
            mean, sd = get_mean_and_sd(list_similar=similars)
            mean = -mean
            good_days = np.where(np.logical_and(abs(mean) > setting.mean, sd > setting.sd))[0]
            order = models.Order.objects.update_or_create(time_marker=time_marker, strategy=strategy)[0]
            history = len(similars)
            if  history >= setting.min_similar and good_days.size:
                n = good_days[-1]
                forecast = abs(mean[n])
                is_buy = mean[n] > 0
                defaults = {
                    "n": n,
                    "forecast": forecast,
                    "is_buy": is_buy,
                    "status_id": 1,
                    "time_marker": time_marker,
                    "history": history,
                    "mean": mean[n],
                    "sd": sd[n]
                }
                models.Result.objects.update_or_create(order=order, defaults=defaults)


def worker_result():
    for result in models.Result.objects.filter(status_id=1):
        order = result.order
        strategy = order.strategy
        setting = strategy.setting
        currency = strategy.currency
        print(currency, result.time_marker)
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = next(currency.left(time_marker=order.time_marker, n=1))
        take = start_bar.close + setting.take * atr
        stop = start_bar.close - setting.stop * atr
        for bar in history_models.Bar.objects.filter(time_marker__time_marker__gt=result.time_marker.time_marker, currency=currency):
            result.time_marker = bar.time_marker
            if result.is_buy:
                result.profit = round((bar.close - start_bar.close) / atr, 2)
                if bar.low < stop:
                    result.profit = round((stop - start_bar.close) / atr, 2)
                    result.status_id = 2
                    break
                if bar.high > take:
                    result.profit = round((take - start_bar.close) / atr, 2)
                    result.status_id = 3
                    break
                if get_working_bars(start_bar.time_marker.time_marker, bar.time_marker.time_marker) >= order.result.n - 1:
                    result.status_id = 4
                    break
            else:
                result.profit = round(-(bar.close - start_bar.close) / atr, 2)
                if bar.low < stop:
                    result.profit = round(-(stop - start_bar.close) / atr, 2)
                    result.status_id = 2
                    break
                if bar.high > take:
                    result.profit = round(-(take - start_bar.close) / atr, 2)
                    result.status_id = 3
                    break
                if get_working_bars(start_bar.time_marker.time_marker, bar.time_marker.time_marker) >= order.result.n - 1:
                    result.status_id = 4
                    break
        result.save()
