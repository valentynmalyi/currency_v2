from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=50, blank=False, db_index=True, unique=True)
    abs_correlation = models.FloatField()
    n = models.PositiveSmallIntegerField()
    history_size = models.PositiveSmallIntegerField()
    min_similar = models.PositiveSmallIntegerField()
    take = models.FloatField()
    mean_min = models.FloatField()
    sd_min = models.FloatField()
    mean_max = models.FloatField()
    sd_max = models.FloatField()
    n_min = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "first_settings"


class Strategy(models.Model):
    currency = models.ForeignKey("history.Currency", on_delete=models.CASCADE)
    setting = models.ForeignKey("Setting", on_delete=models.CASCADE)

    class Meta:
        db_table = "first_strategies"


class Result(models.Model):
    order = models.OneToOneField("Order", on_delete=models.CASCADE)
    is_buy = models.BooleanField()
    n = models.PositiveSmallIntegerField()
    forecast = models.FloatField()
    time_marker = models.ForeignKey("history.TimeMarker", on_delete=models.CASCADE)
    profit = models.FloatField(default=0)
    status = models.ForeignKey("history.OrderStatus", on_delete=models.CASCADE, default=1)
    sd = models.FloatField()

    class Meta:
        db_table = "first_results"
        ordering = ["time_marker"]


class Order(models.Model):
    time_marker = models.ForeignKey("history.TimeMarker", on_delete=models.CASCADE)
    strategy = models.ForeignKey("Strategy", on_delete=models.CASCADE)
    history = models.IntegerField()

    class Meta:
        db_table = "first_orders"
        unique_together = [("strategy", "time_marker")]
        ordering = ["time_marker"]

    def __str__(self):
        return f"{self.time_marker}"
