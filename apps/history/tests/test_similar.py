import numpy as np

from django.test import TestCase
from datetime import date

from apps.history.services.similar import Similar, get_mean_and_sd
from apps.history.models import Currency, TimeMarker, Bar


class SimilarTestCase(TestCase):
    def setUp(self):
        self.currency = Currency.objects.create(first="eur", second="usd")

        self.time_markers = {
            1: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=1)),
            2: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=2)),
            3: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=3)),
            4: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=4)),
            5: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=5)),
            6: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=6)),
            7: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=7)),
            8: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=8)),
            9: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=9)),
            10: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=10)),
            11: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=11)),
            12: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=12)),
            13: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=13)),
            14: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=14)),
            15: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=15)),
            16: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=16)),
            17: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=17)),
            18: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=18)),
            19: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=19)),
            20: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=20)),
            21: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=21)),
            22: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=22)),
            23: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=23)),
            24: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=24)),
            25: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=25)),
            26: TimeMarker.objects.create(time_marker=date(year=2011, month=1, day=26)),

            101: TimeMarker.objects.create(time_marker=date(year=2012, month=1, day=1)),
            102: TimeMarker.objects.create(time_marker=date(year=2012, month=1, day=2)),
            103: TimeMarker.objects.create(time_marker=date(year=2012, month=1, day=3)),
            104: TimeMarker.objects.create(time_marker=date(year=2012, month=1, day=4)),
            105: TimeMarker.objects.create(time_marker=date(year=2012, month=1, day=5))
        }

        self.bars = {
            1: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[1], high=2.5, low=0.5, close=1),
            2: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[2], high=3, low=1, close=2),
            3: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[3], high=4, low=2, close=3),
            4: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[4], high=5, low=3, close=4),
            5: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[5], high=5, low=3, close=3.5),
            6: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[6], high=5, low=3, close=4),
            7: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[7], high=5, low=3, close=3.8),
            8: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[8], high=6, low=4, close=5.4),
            9: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[9], high=6, low=4, close=5),
            10: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[10], high=7, low=5, close=6),
            11: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[11], high=8, low=6, close=7),
            12: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[12], high=9, low=7, close=8),
            13: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[13], high=9, low=7, close=7.3),
            14: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[14], high=9, low=7, close=8.5),
            15: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[15], high=9, low=7, close=7.4),
            16: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[16], high=10, low=8, close=9.4),
            17: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[17], high=10, low=8, close=9),
            18: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[18], high=11, low=9, close=10),
            19: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[19], high=12, low=10, close=11),
            20: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[20], high=13, low=11, close=12),
            21: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[21], high=13, low=11, close=11.3),
            22: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[22], high=13, low=11, close=12.5),
            23: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[23], high=13, low=11, close=11.7),
            24: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[24], high=14, low=12, close=13.6),
            25: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[25], high=14, low=12, close=12.5),
            26: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[26], high=14, low=12, close=13.3),

            101: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[101], high=1.1, low=0.9, close=1),
            102: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[102], high=2.1, low=1.9, close=2),
            103: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[103], high=3.1, low=2.9, close=3),
            104: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[104], high=4.1, low=3.9, close=4),
            105: Bar.objects.create(currency=self.currency, time_marker=self.time_markers[105], high=5.1, low=4.9, close=5)
        }

    def test_get_similar_items(self):
        root_bar = self.bars[105]
        n = 4
        history_size = len(self.bars)
        abs_correlation = 0.99
        first = list(Similar.get_similar_items(root_bar=root_bar, n=n, history_size=history_size, abs_correlation=abs_correlation))
        second = [
            Similar(root_bar=root_bar, correlation=1.2, n=n, bar=self.bars[5]),
            Similar(root_bar=root_bar, correlation=2.3, n=n, bar=self.bars[13]),
            Similar(root_bar=root_bar, correlation=3.4, n=n, bar=self.bars[21])
        ]
        self.assertListEqual(first, second)

    def test_profit(self):
        correlation = 0.5
        n = 4

        bar = self.bars[1]
        similar = Similar(root_bar=bar, bar=bar, correlation=correlation, n=n)
        self.assertRaises(StopIteration, similar.profit)

        bar = self.bars[2]
        similar = Similar(root_bar=bar, bar=bar, correlation=correlation, n=n)
        first = similar.profit()
        second = np.array([0.5, 1, 1.5, 1.25])
        self.assertTrue(np.isclose(first, second).all())

        bar = self.bars[4]
        similar = Similar(root_bar=bar, bar=bar, correlation=-correlation, n=n)
        first = similar.profit()
        second = - np.array([0.5, 0.25, 0.5, 0.4])
        self.assertTrue(np.isclose(first, second).all())

    def test_get_mean_and_sd(self):
        bar = self.bars[105]
        n = 4
        history_size = len(self.bars)
        abs_correlation = 0.95

        list_similar = list(Similar.get_similar_items(root_bar=bar, n=n, history_size=history_size, abs_correlation=abs_correlation))
        mean_first, sd_first = get_mean_and_sd(list_similar=list_similar)
        mean_second = np.array([-0.31666667, 0.16666667, -0.18333333, 0.73333333])
        sd_second = np.array([6.71751442, 1.41421356, 2.15727749, 15.55634919])
        self.assertTrue(np.isclose(mean_first, mean_second).all())
        self.assertTrue(np.isclose(sd_first, sd_second).all())
