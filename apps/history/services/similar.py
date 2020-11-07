import numpy as np

from collections import deque
from typing import Iterator, List

from apps.history.models import Bar


class Similar:

    def __init__(self, root_bar: Bar, bar: Bar, correlation: float, n: int):
        self.root_bar = root_bar
        self.bar = bar
        self.correlation = correlation
        self.n = n

    def __repr__(self):
        return f"Similar({self.root_bar}|{self.bar},{self.correlation:+03.2f})"

    def __eq__(self, other: "Similar"):
        return self.bar == other.bar and self.root_bar == self.root_bar and self.n == other.n

    @classmethod
    def get_similar_items(cls, root_bar: Bar, n: int, history_size: int, abs_correlation: float) -> Iterator["Similar"]:
        """situations are similar from point in history by correlation coefficient"""
        closes_array = root_bar.currency.get_closes_array(time_marker=root_bar.time_marker, n=n)
        deq = deque(maxlen=n)
        correlation = None
        yield_next_bar = False
        shifted_time_marker = root_bar.time_marker.get_left_shift(time_marker=root_bar.time_marker, shift_step=2 * n)
        for bar in root_bar.currency.left(time_marker=shifted_time_marker, n=history_size):
            if yield_next_bar:
                yield cls(root_bar=root_bar, bar=bar, correlation=correlation, n=n)
                yield_next_bar = False
            deq.append(bar.close)
            if len(deq) < n:
                continue
            correlation = np.corrcoef(closes_array, deq)[0, 1]
            if abs(correlation) > abs_correlation:
                yield_next_bar = True

    def profit(self) -> np.array:
        """array profits in atr"""
        close = []
        first = next(self.bar.currency.left(time_marker=self.bar.time_marker, n=1)).close
        atr = self.bar.currency.atr(time_marker=self.bar.time_marker)
        for bar in self.bar.currency.right(time_marker=self.bar.time_marker, n=self.n):
            if self.correlation >= 0:
                close.append((bar.close - first) / atr)
            else:
                close.append(-(bar.close - first) / atr)
        return np.array(close)


def get_mean_and_sd(list_similar: List[Similar]):
    """get mean and sd from similar list"""
    list_profits = []
    for similar in list_similar:
        list_profits.append(similar.profit())
    if len(list_profits) > 2:
        mean = np.mean(list_profits, axis=0)
        sd = np.std(list_profits, axis=0)
        return mean, abs(mean) / sd
    else:
        return np.array([]), np.array([])
