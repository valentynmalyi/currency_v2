from django.db import models


class Order(models.Model):
    login = models.IntegerField(db_index=True)
    time_marker = models.ForeignKey("history.TimeMarker", on_delete=models.CASCADE)
    first = models.ForeignKey("first.Order", on_delete=models.CASCADE)
    status = models.ForeignKey("history.OrderStatus", on_delete=models.CASCADE)
