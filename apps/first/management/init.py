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
        "mean": 0.8,
        "sd": 0.4
    }
    models.Setting.objects.update_or_create(name="classic", defaults=defaults)


def init_strategy() -> None:
    init_settings()
    history_init.init()

    eur = Currency.objects.get(first="eur", second="usd")
    gbp = Currency.objects.get(first="gbp", second="usd")
    jpy = Currency.objects.get(first="usd", second="jpy")
    setting = models.Setting.objects.get(name="classic")

    models.Strategy.objects.update_or_create(currency=eur, setting=setting)
    models.Strategy.objects.update_or_create(currency=gbp, setting=setting)
    models.Strategy.objects.update_or_create(currency=jpy, setting=setting)


def init_orders() -> None:
    OrderStatus.objects.update_or_create(id=1, defaults={"name": "open"})
    OrderStatus.objects.update_or_create(id=2, defaults={"name": "stop loss"})
    OrderStatus.objects.update_or_create(id=3, defaults={"name": "take profit"})
    OrderStatus.objects.update_or_create(id=4, defaults={"name": "time stamp"})


def init():
    init_strategy()
    init_orders()
