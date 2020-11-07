# noinspection PyUnresolvedReferences
import scripts.django_init

from apps.history.models import Currency, OrderStatus
from apps.first.models import Setting, Strategy

eur = Currency.objects.update_or_create(first="eur", second="usd")[0]
Currency.objects.update_or_create(first="gbp", second="usd")
Currency.objects.update_or_create(first="nzd", second="usd")
Currency.objects.update_or_create(first="aud", second="usd")
Currency.objects.update_or_create(first="usd", second="jbp")
Currency.objects.update_or_create(first="usd", second="cad")
Currency.objects.update_or_create(first="usd", second="chf")

setting = Setting.objects.update_or_create(
    name="classic", abs_correlation=0.85, n=50, history_size=2500, min_similar=20, stop=10, take=10, mean=0.8, sd=0.4)[0]
Strategy.objects.update_or_create(currency=eur, setting=setting)

OrderStatus.objects.update_or_create(id=1, name="open")
OrderStatus.objects.update_or_create(id=2, name="stop loss")
OrderStatus.objects.update_or_create(id=3, name="take profit")
OrderStatus.objects.update_or_create(id=4, name="time stamp")
