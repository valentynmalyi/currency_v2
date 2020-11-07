from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=50, blank=False, db_index=True, unique=True)
    abs_correlation = models.FloatField()
    n = models.PositiveSmallIntegerField()
    history_size = models.PositiveSmallIntegerField()
    min_similar = models.PositiveSmallIntegerField()
    stop = models.FloatField()
    take = models.FloatField()
    mean = models.FloatField()
    sd = models.FloatField()

    class Meta:
        db_table = "first_settings"


class Strategy(models.Model):
    currency = models.ForeignKey("history.Currency", on_delete=models.CASCADE)
    setting = models.ForeignKey("Setting", on_delete=models.CASCADE)

    class Meta:
        db_table = "first_strategies"


class OrderSetting(models.Model):
    close_n = models.PositiveSmallIntegerField()
    forecast = models.FloatField()
    is_buy = models.BooleanField()
    result = models.FloatField(default=None, null=True)
    current_result = models.FloatField(default=None, null=True)

    class Meta:
        db_table = "first_order_settings"


class Order(models.Model):
    strategy = models.ForeignKey("Strategy", on_delete=models.CASCADE)
    time_marker = models.ForeignKey("history.TimeMarker", on_delete=models.CASCADE)
    order_setting = models.ForeignKey("OrderSetting", on_delete=models.CASCADE, default=None, null=True)
    is_close = models.BooleanField(default=None, null=True, db_index=True)

    class Meta:
        db_table = "first_orders"
        unique_together = [("strategy", "time_marker")]
        index_together = [("order_setting", "is_close")]


class Result(models.Model):
    close_n = models.ForeignKey("Order", on_delete=models.CASCADE)
    time_marker = models.ForeignKey("history.TimeMarker", on_delete=models.CASCADE)
    result = models.FloatField()
    status = models.ForeignKey("history.OrderStatus", on_delete=models.CASCADE)

    class Meta:
        db_table = "first_results"
