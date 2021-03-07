from apps.history.models import Currency


def init_currency():
    Currency.objects.update_or_create(first="eur", second="usd")
    Currency.objects.update_or_create(first="gbp", second="usd")
    Currency.objects.update_or_create(first="nzd", second="usd")
    Currency.objects.update_or_create(first="aud", second="usd")
    Currency.objects.update_or_create(first="usd", second="jpy")
    Currency.objects.update_or_create(first="usd", second="cad")


def init():
    init_currency()
