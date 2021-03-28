from apps.history.models import Currency, OrderStatus
from apps.first import models

from apps.history.management import init as history_init


def init_settings() -> None:
    defaults = {
        "abs_correlation": 0.85,
        "n": 50,
        "history_size": 2500,
        "min_similar": 20,
        "stop": 10,
        "take": 10,
        "mean_min": 0.8,
        "sd_min": 0.4
    }
    models.Setting.objects.update_or_create(name="c85", defaults=defaults)
    defaults = {
        "abs_correlation": 0.95,
        "n": 50,
        "history_size": 2500,
        "min_similar": 20,
        "stop": 10,
        "take": 10,
        "mean_min": 0.8,
        "sd_min": 0.4
    }
    models.Setting.objects.update_or_create(name="c95", defaults=defaults)
    defaults = {
        "abs_correlation": 0.9,
        "n": 50,
        "history_size": 2500,
        "min_similar": 20,
        "stop": 10,
        "take": 10,
        "mean_min": 0.8,
        "sd_min": 0.4
    }
    models.Setting.objects.update_or_create(name="c90", defaults=defaults)


def init_strategy() -> None:
    init_settings()
    history_init.init()

    eur = Currency.objects.get(first="eur", second="usd")
    gbp = Currency.objects.get(first="gbp", second="usd")
    jpy = Currency.objects.get(first="usd", second="jpy")
    cad = Currency.objects.get(first="usd", second="cad")
    aud = Currency.objects.get(first="aud", second="usd")
    nzd = Currency.objects.get(first="nzd", second="usd")
    setting = models.Setting.objects.get(name="c85")

    models.Strategy.objects.update_or_create(currency=eur, setting=setting)
    models.Strategy.objects.update_or_create(currency=gbp, setting=setting)
    models.Strategy.objects.update_or_create(currency=jpy, setting=setting)
    models.Strategy.objects.update_or_create(currency=cad, setting=setting)
    models.Strategy.objects.update_or_create(currency=aud, setting=setting)
    models.Strategy.objects.update_or_create(currency=nzd, setting=setting)

    setting = models.Setting.objects.get(name="c90")

    models.Strategy.objects.update_or_create(currency=eur, setting=setting)
    models.Strategy.objects.update_or_create(currency=gbp, setting=setting)
    models.Strategy.objects.update_or_create(currency=jpy, setting=setting)
    models.Strategy.objects.update_or_create(currency=cad, setting=setting)
    models.Strategy.objects.update_or_create(currency=aud, setting=setting)
    models.Strategy.objects.update_or_create(currency=nzd, setting=setting)

    setting = models.Setting.objects.get(name="c99")

    models.Strategy.objects.update_or_create(currency=eur, setting=setting)
    models.Strategy.objects.update_or_create(currency=gbp, setting=setting)
    models.Strategy.objects.update_or_create(currency=jpy, setting=setting)
    models.Strategy.objects.update_or_create(currency=cad, setting=setting)
    models.Strategy.objects.update_or_create(currency=aud, setting=setting)
    models.Strategy.objects.update_or_create(currency=nzd, setting=setting)


def init_orders() -> None:
    OrderStatus.objects.update_or_create(id=1, defaults={"name": "open"})
    OrderStatus.objects.update_or_create(id=2, defaults={"name": "stop loss"})
    OrderStatus.objects.update_or_create(id=3, defaults={"name": "take profit"})
    OrderStatus.objects.update_or_create(id=4, defaults={"name": "time stamp"})


def init():
    init_strategy()
    init_orders()
