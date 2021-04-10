from datetime import datetime

import MetaTrader5 as mt5

from django.conf import settings

from apps.history import models
from apps.history.models import TimeMarker, Bar


def main():
    mt5.initialize()
    mt5.login(settings.METATRADE.LOGIN, password=settings.METATRADE.PASSWORD, server=settings.METATRADE.SERVER)
    for currency in models.Currency.objects.all().iterator():  # type: models.Currency
        print(currency)
        name = f"{currency.first}{currency.second}".upper()
        latest = models.Bar.objects.filter(currency=currency).latest("time_marker__time_marker")
        latest_datetime = datetime.combine(latest.time_marker.time_marker, datetime.min.time())
        for item in mt5.copy_rates_range(name, mt5.TIMEFRAME_D1, latest_datetime, datetime.utcnow()):
            close = item["close"]
            high = item["high"]
            low = item["low"]
            t = datetime.utcfromtimestamp(item["time"]).date()
            if t.weekday() in {6, 5}:
                continue
            time_marker = TimeMarker.objects.get_or_create(time_marker=t)[0]
            print(currency, time_marker)
            Bar.objects.update_or_create(currency=currency, time_marker=time_marker, defaults={"close": close, "high": high, "low": low})
