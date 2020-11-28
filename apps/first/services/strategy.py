import numpy as np
from django.db.models import Max
from django.conf import settings

# noinspection PyUnresolvedReferences
import scripts.django_init
from apps.history.models import Currency, TimeMarker, Bar
from apps.first.models import Strategy, Setting, Order, Result
from apps.history.services.similar import Similar, get_mean_and_sd

if __name__ == '__main__':
    currency = Currency.objects.get(first="eur", second="usd")
    setting = Setting.objects.get(name="classic")
    strategy = Strategy.objects.get(currency=currency, setting=setting)
    data_time = settings.START_DATE

    max_time_marker = Order.objects.aggregate(Max("time_marker"))["time_marker__max"]
    if max_time_marker:
        data_time = TimeMarker.objects.get(id=max_time_marker).time_marker

    for time_marker in TimeMarker.objects.filter(time_marker__gt=data_time).order_by("time_marker"):
        print(time_marker)
        root_bar = Bar.objects.get(time_marker=time_marker, currency=currency)
        list_similar = list(Similar.get_similar_items(
            root_bar=root_bar, n=setting.n, history_size=setting.history_size, abs_correlation=setting.abs_correlation))
        mean, sd = get_mean_and_sd(list_similar=list_similar)
        mean = -mean
        good_days = np.where(np.logical_and(abs(mean) > setting.mean, sd > setting.sd))[0]
        if len(list_similar) >= setting.min_similar and good_days.size:
            n = good_days[-1]
            forecast = abs(mean[n])
            is_buy = mean[n] > 0
            defaults = {"n": n, "forecast": forecast, "is_buy": is_buy}
            result = Result.objects.update_or_create(time_marker=time_marker, defaults=defaults)[0]

            defaults = {"result": result}
            Order.objects.update_or_create(time_marker=time_marker, strategy=strategy, defaults=defaults)
        else:
            Order.objects.update_or_create(time_marker=time_marker, strategy=strategy)
