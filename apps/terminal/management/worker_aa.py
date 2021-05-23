from datetime import datetime

import MetaTrader5 as Mt5

from django.conf import settings

from apps.first import models as first_models
from apps.terminal import models


def main():
    Mt5.initialize()
    Mt5.login(settings.METATRADE.LOGIN, password=settings.METATRADE.PASSWORD, server=settings.METATRADE.SERVER)

    for deal in models.Deal.objects.filter(status__id=1, first__time_marker__time_marker=datetime(2020, 8, 20)):  # type: models.Deal
        result = deal.first
        if result.is_open():
            deal.close_first()

    for result in first_models.Result.objects.filter(status__id=1,
                                                     first__time_marker__time_marker=datetime(2020, 8, 20)):  # type: first_models.Result
        if models.Deal.objects.filter(result=result).exist():
            continue
        order = result.order
        if order.time_marker == result.time_marker:
            models.Deal.open_first(result=result)
