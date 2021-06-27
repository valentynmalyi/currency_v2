import numpy as np
import logging

from django.conf import settings

from apps.history import models as history_models
from apps.first import models
from apps.history.services.similar import Similar, get_mean_and_sd
from currency.utils import get_working_bars

log_worker_order = logging.getLogger("worker_order")
log_worker_result = logging.getLogger("worker_result")


def worker_order():
    setting = models.Setting.objects.get(name="c95")
    for strategy in models.Strategy.objects.filter(setting=setting):
        currency = strategy.currency
        data_time = settings.START_DATE
        query_set = history_models.TimeMarker.objects.filter(time_marker__gte=data_time)
        query_set = query_set.exclude(time_marker__in=models.Order.objects.filter(strategy=strategy).values("time_marker__time_marker"))
        for time_marker in query_set.iterator():
            root_bar = history_models.Bar.objects.get(time_marker=time_marker, currency=currency)
            similars = list(Similar.get_similar_items(
                root_bar=root_bar, n=setting.n, history_size=setting.history_size, abs_correlation=setting.abs_correlation))
            mean, sd = get_mean_and_sd(list_similar=similars)
            mean = -mean
            abs_mean = abs(mean)
            logical = (setting.mean_min < abs_mean) & (abs_mean < setting.mean_max) & (setting.sd_min < sd) & (sd < setting.sd_max)
            good_days = np.where(logical)[0]
            history = len(similars)
            log_worker_order.debug({
                "currency": currency,
                "time_marker": time_marker,
            })
            defaults = {
                "history": history
            }
            order = models.Order.objects.update_or_create(time_marker=time_marker, strategy=strategy, defaults=defaults)[0]
            if history < setting.min_similar or not good_days.size:
                log_worker_order.debug({
                    "status": "Bad size or min_similar",
                    "history": history
                })
                log_worker_order.debug("")
                continue
            n = good_days[-1]
            if n < setting.n_min:
                log_worker_order.debug({
                    "status": "Bad n_min",
                    "n": n
                })
                log_worker_order.debug("")
                continue
            atr = currency.atr(time_marker=order.time_marker)
            start_bar = currency.get_start_bar(time_marker=order.time_marker)
            is_buy = mean[n] > 0
            sl = start_bar.close - order.strategy.setting.take * atr
            tp = start_bar.close + order.strategy.setting.take * atr
            if not is_buy:
                tp, sl = sl, tp
            defaults = {
                "n": n,
                "forecast": abs_mean[n],
                "is_buy": is_buy,
                "status_id": 1,
                "time_marker": time_marker,
                "sd": sd[n],
                "atr": atr,
                "volume": settings.METATRADE.FIRST_VOLUME * start_bar.close / atr,
                "sl": sl,
                "tp": tp
            }
            log_worker_order.debug({
                "status": "save",
            })
            models.Result.objects.update_or_create(order=order, defaults=defaults)
            log_worker_order.debug("")


def worker_result():
    log_worker_result.debug("start")
    for result in models.Result.objects.filter(status_id=1):
        order = result.order
        strategy = order.strategy
        setting = strategy.setting
        currency = strategy.currency
        log_worker_result.debug({"currency": currency, "time_marker": result.time_marker})
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = next(currency.left(time_marker=order.time_marker, n=1))
        price_up = start_bar.close + setting.take * atr
        price_down = start_bar.close - setting.take * atr
        for bar in history_models.Bar.objects.filter(time_marker__time_marker__gt=result.time_marker.time_marker, currency=currency):
            result.time_marker = bar.time_marker
            log_worker_result.debug({"bar": bar.time_marker})
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
        log_worker_result.debug("")
        result.save()
