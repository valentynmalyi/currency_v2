import logging

import MetaTrader5 as Mt5

from django.conf import settings

from apps.terminal import models

log = logging.getLogger("worker_first_close")


def main():
    Mt5.initialize()
    Mt5.login(settings.METATRADE.LOGIN, password=settings.METATRADE.PASSWORD, server=settings.METATRADE.SERVER)
    log.debug("start")
    for deal in models.Deal.objects.filter(status__id=1):  # type: models.Deal
        log.debug({"deal": deal})
        result = deal.first
        if result.is_open():
            deal.close_first()
    log.debug("end")
