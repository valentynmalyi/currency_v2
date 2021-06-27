import logging

from datetime import datetime

import MetaTrader5 as Mt5

from django.conf import settings

from apps.history import models
from apps.history.models import TimeMarker, Bar

log = logging.getLogger("history")


def main():
    Mt5.initialize()
    Mt5.login(settings.METATRADE.LOGIN, password=settings.METATRADE.PASSWORD, server=settings.METATRADE.SERVER)
    for currency in models.Currency.objects.all().iterator():  # type: models.Currency
        name = f"{currency.first}{currency.second}".upper()
        log.debug({"currency": name})
        latest = models.Bar.objects.filter(currency=currency).latest("time_marker__time_marker")
        latest_datetime = datetime.combine(latest.time_marker.time_marker, datetime.min.time())
        date_to = datetime.utcnow()
        items = Mt5.copy_rates_range(name, Mt5.TIMEFRAME_D1, latest_datetime, date_to)
        if items is None:
            continue
        for item in items:
            close = item["close"]
            high = item["high"]
            low = item["low"]
            t = datetime.utcfromtimestamp(item["time"]).date()
            if t.weekday() in {6, 5}:
                continue
            if t > date_to.date():
                continue
            time_marker = TimeMarker.objects.get_or_create(time_marker=t)[0]
            log.debug({"time_marker": time_marker})
            Bar.objects.update_or_create(currency=currency, time_marker=time_marker, defaults={"close": close, "high": high, "low": low})
            log.debug("")
