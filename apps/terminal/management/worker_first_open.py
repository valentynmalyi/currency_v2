import logging

import MetaTrader5 as Mt5

from django.conf import settings

from apps.first import models as first_models
from apps.terminal import models

log = logging.getLogger("worker_first_open")


def main():
    Mt5.initialize()
    Mt5.login(settings.METATRADE.LOGIN, password=settings.METATRADE.PASSWORD, server=settings.METATRADE.SERVER)
    log.debug("start")
    for result in first_models.Result.objects.filter(status__id=1):  # type: first_models.Result
        log.debug({"result": result})
        if models.Deal.objects.filter(first=result).exists():
            log.debug("")
            continue
        order = result.order
        if order.time_marker == result.time_marker:
            models.Deal.open_first(result=result)
            log.debug({"status": "open"})
    log.debug("end")
