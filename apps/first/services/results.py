# from django.db.models import Max
# noinspection PyUnresolvedReferences
import scripts.django_init
from apps.history.models import Currency, TimeMarker, Bar
from apps.first.models import Strategy, Setting, Order, OrderSetting
from apps.history.services.similar import Similar, get_mean_and_sd


if __name__ == '__main__':
    currency = Currency.objects.get(first="eur", second="usd")
    setting = Setting.objects.get(name="classic")
    strategy = Strategy.objects.get(currency=currency, setting=setting)

    for order in Order.objects.filter(order_setting__isnull=False, is_close__isnull=True):
        order_setting = order.order_setting
        print(order)
        time_markers = TimeMarker.objects.filter(time_marker__gt=order.time_marker.time_marker).order_by("time_marker")
        for time_marker in time_markers[:order_setting.close_n + 1]:
            bar = Bar.objects.get(time_marker=time_marker, currency=currency)

            close = next(currency.left(time_marker=time_marker, n=1)).close
            plus = currency.atr(time_marker=time_marker) * close
            if order_setting.is_buy:
                take = close + plus * setting.take
                stop = close - plus * setting.stop
            else:
                take = close - plus * setting.take
                stop = close + plus * setting.stop
            print(take, stop)


