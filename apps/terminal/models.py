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
    sl = models.IntegerField()
    tp = models.IntegerField()

    @classmethod
    def open_first(cls, result: first_models.Result):
        first_order: first_models.Order = result.order
        if result.is_buy:
            cls.open_first_buy(order=first_order)
            sl = cls.open_sell_stop(order=first_order)
            tp = cls.open_sell_limit(order=first_order)
        else:
            cls.open_first_sell(order=first_order)
            sl = cls.open_buy_stop(order=first_order)
            tp = cls.open_buy_limit(order=first_order)
        status = history_models.OrderStatus.objects.get(id=1)
        return cls.objects.create(login=settings.METATRADE.LOGIN, first=result, status=status, tp=tp, sl=sl)

    def close_first(self):
        is_open = True
        is_open = self.close_pending(ticket=self.sl) & is_open
        is_open = self.close_pending(ticket=self.tp) & is_open

        if not is_open:
            return

        self.close_order()



    @classmethod
    def open_first_buy(cls, order: first_models.Order):
        currency: history_models.Currency = order.strategy.currency
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = currency.get_start_bar(time_marker=order.time_marker)
        atr_pure = atr / start_bar.close
        volume = round(settings.METATRADE.VOLUME / atr_pure, 2)
        type_ = Mt5.ORDER_TYPE_BUY
        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": currency.symbol,
            "volume": volume,
            "type": type_,
            "type_filling": Mt5.ORDER_FILLING_FOK,
        }
        cls.order_send(request=request)

    @classmethod
    def open_first_sell(cls, order: first_models.Order):
        currency: history_models.Currency = order.strategy.currency
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = currency.get_start_bar(time_marker=order.time_marker)
        atr_pure = atr / start_bar.close
        volume = round(settings.METATRADE.VOLUME / atr_pure, 2)
        type_ = Mt5.ORDER_TYPE_SELL
        request = {
            "action": Mt5.TRADE_ACTION_DEAL,
            "symbol": currency.symbol,
            "volume": volume,
            "type": type_,
            "type_filling": Mt5.ORDER_FILLING_FOK,
        }
        cls.order_send(request=request)

    @classmethod
    def open_buy_limit(cls, order: first_models.Order):
        currency: history_models.Currency = order.strategy.currency
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = currency.get_start_bar(time_marker=order.time_marker)
        atr_pure = atr / start_bar.close
        volume = round(settings.METATRADE.VOLUME / atr_pure, 2)
        type_ = Mt5.ORDER_TYPE_BUY_LIMIT
        price = start_bar.close - order.strategy.setting.take * atr_pure
        request = {
            "action": Mt5.TRADE_ACTION_PENDING,
            "symbol": currency.symbol,
            "volume": volume,
            "type": type_,
            "price": price
        }

        answer = cls.order_send(request=request)
        return answer.order

    @classmethod
    def open_buy_stop(cls, order: first_models.Order):
        currency: history_models.Currency = order.strategy.currency
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = currency.get_start_bar(time_marker=order.time_marker)
        atr_pure = atr / start_bar.close
        volume = round(settings.METATRADE.VOLUME / atr_pure, 2)
        type_ = Mt5.ORDER_TYPE_BUY_STOP
        price = start_bar.close + order.strategy.setting.take * atr_pure
        request = {
            "action": Mt5.TRADE_ACTION_PENDING,
            "symbol": currency.symbol,
            "volume": volume,
            "type": type_,
            "price": price
        }

        answer = cls.order_send(request=request)
        return answer.order

    @classmethod
    def open_sell_stop(cls, order: first_models.Order):
        currency: history_models.Currency = order.strategy.currency
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = currency.get_start_bar(time_marker=order.time_marker)
        atr_pure = atr / start_bar.close
        volume = round(settings.METATRADE.VOLUME / atr_pure, 2)
        type_ = Mt5.ORDER_TYPE_SELL_STOP
        price = start_bar.close - order.strategy.setting.take * atr_pure
        request = {
            "action": Mt5.TRADE_ACTION_PENDING,
            "symbol": currency.symbol,
            "volume": volume,
            "type": type_,
            "price": price
        }
        answer = cls.order_send(request=request)
        return answer.order

    @classmethod
    def open_sell_limit(cls, order: first_models.Order):
        currency: history_models.Currency = order.strategy.currency
        atr = currency.atr(time_marker=order.time_marker)
        start_bar = currency.get_start_bar(time_marker=order.time_marker)
        atr_pure = atr / start_bar.close
        volume = round(settings.METATRADE.VOLUME / atr_pure, 2)
        type_ = Mt5.ORDER_TYPE_SELL_LIMIT
        price = start_bar.close + order.strategy.setting.take * atr_pure
        request = {
            "action": Mt5.TRADE_ACTION_PENDING,
            "symbol": currency.symbol,
            "volume": volume,
            "type": type_,
            "price": price
        }
        answer = cls.order_send(request=request)
        return answer.order

    @staticmethod
    def is_pending_exist(ticket: int):
        return bool(Mt5.orders_get(ticket=ticket))

    @classmethod
    def close_pending(cls, ticket: int):
        if not cls.is_pending_exist(ticket=ticket):
            return False
        request = {
            "action": Mt5.TRADE_ACTION_REMOVE,
            "order": ticket
        }
        cls.order_send(request=request)
        return True

    @staticmethod
    def order_send(request: dict):
        answer = Mt5.order_send(request)
        if answer.retcode != 10009:
            raise Exception("Mt5 return code is not 10009")
        return answer
