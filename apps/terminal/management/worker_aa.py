from datetime import datetime, timedelta

import MetaTrader5 as Mt5

from django.conf import settings

from apps.history import models as history_models
from apps.first import models as first_models
from apps.terminal import models


def main():
    Mt5.initialize()
    Mt5.login(settings.METATRADE.LOGIN, password=settings.METATRADE.PASSWORD, server=settings.METATRADE.SERVER)

    for result in first_models.Result.objects.filter(first__time_marker__time_marker=datetime(2020, 8, 20)):  # type: first_models.Result
        order: first_models.Order = result.order

        if order.time_marker == result.time_marker:
            models.Deal.open_first(result=result)

    for deal in models.Deal.objects.filter(first__time_marker__time_marker=datetime(2020, 8, 20)):  # type: models.Deal
        result = deal.first

        if result.is_close():
            deal.close_first()
