from django.conf import settings
from django.db import models
import MetaTrader5 as Mt5

from apps.history import models as history_models
from apps.first import models as first_models

Mt5.initialize()
Mt5.login(settings.METATRADE.LOGIN, password=settings.METATRADE.PASSWORD, server=settings.METATRADE.SERVER)


class Deal(models.Model):
    login = models.IntegerField(db_index=True)
    first = models.ForeignKey(first_models.Result, on_delete=models.CASCADE, default=None)
    status = models.ForeignKey(history_models.OrderStatus, on_delete=models.CASCADE)
    order = models.IntegerField()

    @classmethod
    def open_first(cls, result: first_models.Result):
        order = cls.open_first_order(result=result)
        status = history_models.OrderStatus.objects.get(id=1)
        return cls.objects.create(login=settings.METATRADE.LOGIN, first=result, status=status, order=order)

    @classmethod
    def open_first_order(cls, result: first_models.Result):
        currency: history_models.Currency = result.order.strategy.currency
        type_ = cls.get_type(is_buy=result.is_buy)
        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": currency.symbol,
            "volume":  round(result.volume, 2),
            "type": type_,
            "type_filling": Mt5.ORDER_FILLING_FOK,
            "sl": result.sl,
            "tp": result.tp
        }
        buy = cls.order_send(request=request)
        return buy.order

    @staticmethod
    def get_type(is_buy: bool):
        if is_buy:
            return Mt5.ORDER_TYPE_BUY
        return Mt5.ORDER_TYPE_SELL

    @staticmethod
    def order_send(request: dict):
        answer = Mt5.order_send(request)
        if answer.retcode != 10009:
            raise Exception("Mt5 return code is not 10009")
        return answer

    def close_first(self):
        first = self.first
        type_ = self.get_type(is_buy=not first.is_buy)
        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "position": self.order,
            "volume": round(self.first.volume, 2),
            "type": type_,
            "type_filling": Mt5.ORDER_FILLING_FOK,
            "symbol": self.first.order.strategy.currency.symbol
        }
        self.order_send(request=request)
        self.status = self.first.status
        self.save()
