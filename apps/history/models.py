import numpy as np
from datetime import date
from typing import Iterator
from django.db import models


class Bar(models.Model):
    time_marker = models.ForeignKey("TimeMarker", on_delete=models.CASCADE)
    currency = models.ForeignKey("Currency", on_delete=models.CASCADE)
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()

    class Meta:
        db_table = "bars"
        unique_together = [("time_marker", "currency")]
        index_together = [("time_marker", "currency")]

    def __str__(self):
        return f"Bar({self.currency},{self.time_marker})"


class TimeMarker(models.Model):
    time_marker = models.DateField(db_index=True, unique=True)

    class Meta:
        db_table = "time_markers"

    def __str__(self):
        return f"{self.time_marker}"

    @classmethod
    def get_left_shift(cls, time_marker: "TimeMarker", shift_step: int) -> "TimeMarker":
        time_markers = cls.objects.filter(time_marker__lt=time_marker.time_marker).order_by("-time_marker")[shift_step:]
        if time_markers:
            return time_markers.first()
        else:
            return time_marker


class Currency(models.Model):
    first = models.CharField(max_length=3, null=False, blank=False)
    second = models.CharField(max_length=3, null=False, blank=False)

    class Meta:
        db_table = "currencies"
        unique_together = [("first", "second")]
        index_together = [("first", "second")]

    def __str__(self):
        return f"{self.first}_{self.second}"

    def left(self, time_marker: TimeMarker, n: int) -> Iterator[Bar]:
        yield from reversed(Bar.objects.filter(time_marker__lt=time_marker, currency=self).order_by("-time_marker")[:n])

    def right(self, time_marker: TimeMarker, n: int) -> Iterator[Bar]:
        yield from Bar.objects.filter(time_marker__gte=time_marker, currency=self).order_by("time_marker")[:n]

    def atr(self, time_marker: TimeMarker) -> float:
        """calculate atr 5"""
        s = 0
        num = 0
        for bar in self.left(time_marker=time_marker, n=5):
            s += bar.high - bar.low
            num += 1
        if num:
            return s / num
        return 1

    def get_closes_array(self, time_marker: TimeMarker, n: int) -> np.array:
        """calculate array form close values"""
        array = []
        for bar in self.left(time_marker=time_marker, n=n):
            array.append(bar.close)
        return np.array(array)


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, blank=False, db_index=True, unique=True)

    class Meta:
        db_table = "order_statuses"
