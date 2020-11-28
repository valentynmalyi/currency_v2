# from django.db.models import Max
# noinspection PyUnresolvedReferences
import scripts.django_init

from apps.history.models import Currency, Bar
from apps.first.models import Strategy, Setting, Order
from currency.utils import get_working_bars

if __name__ == '__main__':
    currency = Currency.objects.get(first="eur", second="usd")
    setting = Setting.objects.get(name="classic")
    strategy = Strategy.objects.get(currency=currency, setting=setting)

    for order in Order.objects.filter(result__isnull=False, result__status_id=1):
        result = order.profit
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = next(currency.left(time_marker=order.time_marker, n=1))
        take = start_bar.close + setting.take * atr
        stop = start_bar.close - setting.stop * atr
        for bar in Bar.objects.filter(time_marker__time_marker__gte=result.time_marker.time_marker, currency=currency):
            result.time_marker = bar.time_marker
            if result.is_buy:
                result.profit = round((bar.close - start_bar.close) / atr, 2)
                if get_working_bars(start_bar.time_marker.time_marker, bar.time_marker.time_marker) >= order.profit.n:
                    result.status_id = 4
                    break
                if bar.low < stop:
                    result.profit = round((stop - start_bar.close) / atr, 2)
                    result.status_id = 2
                    break
                if bar.high > take:
                    result.profit = round((take - start_bar.close) / atr, 2)
                    result.status_id = 3
                    break
            else:
                result.profit = round(-(bar.close - start_bar.close) / atr, 2)
                if get_working_bars(start_bar.time_marker.time_marker, bar.time_marker.time_marker) >= order.profit.n:
                    result.status_id = 4
                    break
                if bar.low < stop:
                    result.profit = round(-(stop - start_bar.close) / atr, 2)
                    result.status_id = 2
                    break
                if bar.high > take:
                    result.profit = round(-(take - start_bar.close) / atr, 2)
                    result.status_id = 3
                    break
            result.save()
