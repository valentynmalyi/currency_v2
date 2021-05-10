import numpy as np
from django.conf import settings

from apps.history import models as history_models
from apps.first import models
from apps.history.services.similar import Similar, get_mean_and_sd
from currency.utils import get_working_bars


def worker_order():
    setting = models.Setting.objects.get(name="c95")
    for strategy in models.Strategy.objects.filter(setting=setting):
        currency = strategy.currency
        data_time = settings.START_DATE
        query_set = history_models.TimeMarker.objects.filter(time_marker__gte=data_time)
        query_set = query_set.exclude(time_marker__in=models.Order.objects.filter(strategy=strategy).values("time_marker__time_marker"))

        for time_marker in query_set.iterator():
            print(time_marker, currency)
            root_bar = history_models.Bar.objects.get(time_marker=time_marker, currency=currency)
            similars = list(Similar.get_similar_items(
                root_bar=root_bar, n=setting.n, history_size=setting.history_size, abs_correlation=setting.abs_correlation))
            mean, sd = get_mean_and_sd(list_similar=similars)
            mean = -mean
            abs_mean = abs(mean)
            logical = (setting.mean_min < abs_mean) & (abs_mean < setting.mean_max) & (setting.sd_min < sd) & (sd < setting.sd_max)
            good_days = np.where(logical)[0]
            history = len(similars)
            defaults = {
                "history": history
            }
            order = models.Order.objects.update_or_create(time_marker=time_marker, strategy=strategy, defaults=defaults)[0]
            if history < setting.min_similar or not good_days.size:
                continue
            n = good_days[-1]
            if n < setting.n_min:
                continue
            defaults = {
                "n": n,
                "forecast": abs_mean[n],
                "is_buy": mean[n] > 0,
                "status_id": 1,
                "time_marker": time_marker,
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
        price_up = start_bar.close + setting.take * atr
        price_down = start_bar.close - setting.take * atr
        for bar in history_models.Bar.objects.filter(time_marker__time_marker__gt=result.time_marker.time_marker, currency=currency):
            result.time_marker = bar.time_marker
            if result.is_buy:
                result.profit = round((bar.close - start_bar.close) / atr, 2)
                if bar.low < price_down:
                    result.profit = round((price_down - start_bar.close) / atr, 2)
                    result.status_id = 2
                    break
                if bar.high > price_up:
                    result.profit = round((price_up - start_bar.close) / atr, 2)
                    result.status_id = 3
                    break
                if get_working_bars(start_bar.time_marker.time_marker, bar.time_marker.time_marker) >= order.result.n - 1:
                    result.status_id = 4
                    break
            else:
                result.profit = round(-(bar.close - start_bar.close) / atr, 2)
                if bar.low < price_down:
                    result.profit = round(-(price_down - start_bar.close) / atr, 2)
                    result.status_id = 2
                    break
                if bar.high > price_up:
                    result.profit = round(-(price_up - start_bar.close) / atr, 2)
                    result.status_id = 3
                    break
                if get_working_bars(start_bar.time_marker.time_marker, bar.time_marker.time_marker) >= order.result.n - 1:
                    result.status_id = 4
                    break
        result.save()
