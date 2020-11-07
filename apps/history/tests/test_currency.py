import numpy as np

from django.test import TestCase
from datetime import date

from apps.history.models import Currency, Bar, TimeMarker


class CurrencyTestCase(TestCase):
    def setUp(self):
        self.currency = Currency.objects.create(first="eur", second="usd")

        self.time_markers = {
            1: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=1)),
            2: TimeMarker.objects.create(time_marker=date(year=2011, month=2, day=2)),
            3: TimeMarker.objects.create(time_marker=date(year=2011, month=3, day=3)),
            4: TimeMarker.objects.create(time_marker=date(year=2011, month=4, day=4))
        }

        self.bars = {
            1: Bar.objects.create(time_marker=self.time_markers[1], currency=self.currency, high=1.1, low=0.9, close=1),
            2: Bar.objects.create(time_marker=self.time_markers[2], currency=self.currency, high=2.1, low=1.9, close=2),
            3: Bar.objects.create(time_marker=self.time_markers[3], currency=self.currency, high=3.1, low=2.9, close=3),
            4: Bar.objects.create(time_marker=self.time_markers[4], currency=self.currency, high=4.1, low=3.9, close=4)
        }

    def test_left(self):
        time_marker = self.time_markers[3]
        first = list(self.currency.left(time_marker=time_marker, n=1))
        second = [self.bars[2]]
        self.assertListEqual(first, second)

        time_marker = self.time_markers[4]
        first = list(self.currency.left(time_marker=time_marker, n=len(self.bars)))
        second = [self.bars[1], self.bars[2], self.bars[3]]
        self.assertListEqual(first, second)

    def test_right(self):
        time_marker = self.time_markers[2]
        first = list(self.currency.right(time_marker=time_marker, n=2))
        second = [self.bars[2], self.bars[3]]
        self.assertListEqual(first, second)

        time_marker = self.time_markers[2]
        first = list(self.currency.right(time_marker=time_marker, n=len(self.bars)))
        second = [self.bars[2], self.bars[3], self.bars[4]]
        self.assertListEqual(first, second)

    def test_atr(self):
        time_marker = self.time_markers[2]
        first = self.currency.atr(time_marker=time_marker)
        self.assertTrue(np.isclose(first, 0.2))

        time_marker = self.time_markers[1]
        first = self.currency.atr(time_marker=time_marker)
        self.assertEqual(first, 1)

    def test_get_closes_array(self):
        time_marker = self.time_markers[3]
        first = self.currency.get_closes_array(time_marker=time_marker, n=1)
        second = np.array([self.bars[2].close])
        self.assertTrue(np.equal(first, second).all())

        time_marker = self.time_markers[4]
        first = self.currency.get_closes_array(time_marker=time_marker, n=len(self.bars))
        second = np.array([self.bars[1].close, self.bars[2].close, self.bars[3].close])
        self.assertTrue(np.equal(first, second).all())


class TimeMarkerTestCase(TestCase):

    def setUp(self):
        self.time_markers = {
            1: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=1)),
            2: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=2)),
            3: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=3)),
            4: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=4)),
            5: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=5)),
            6: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=6)),
            7: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=7)),
            8: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=8)),
        }

    def test_get_left_shift(self):
        time_marker = self.time_markers[8]
        first = TimeMarker.get_left_shift(time_marker=time_marker, shift_step=4)
        second = self.time_markers[3]
        self.assertEqual(first, second)

        time_marker = self.time_markers[7]
        first = TimeMarker.get_left_shift(time_marker=time_marker, shift_step=3)
        second = self.time_markers[3]
        self.assertEqual(first, second)

        time_marker = self.time_markers[1]
        first = TimeMarker.get_left_shift(time_marker=time_marker, shift_step=1)
        second = self.time_markers[1]
        self.assertEqual(first, second)
