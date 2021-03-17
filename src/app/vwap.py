import bisect
from decimal import Decimal
from typing import List, Collection

from src.app.model import TradingPair, TradingPoint

_ZERO = Decimal(0)


class VWAP:
    """
    Volume Weighted Average Price
    See → https://en.wikipedia.org/wiki/Volume-weighted_average_price
    """

    def __init__(self, trading_pair: TradingPair, max_size=200):
        self._trading_pair = trading_pair
        self._max_size = max_size
        self._points: List[TradingPoint] = []

    def add_point(self, point: TradingPoint):
        if point.pair != self._trading_pair:
            raise ValueError(f'Unsupported trading pair: {point.pair}')

        bisect.insort(self._points, point)

        if len(self._points) > self._max_size:
            self._points.pop(0)

    def current_value(self) -> Decimal:
        price_quantity_sum = _ZERO
        quantity_sum = _ZERO

        for point in self._points:
            price_quantity_sum += point.price * point.quantity
            quantity_sum += point.quantity

        return (price_quantity_sum / quantity_sum) if quantity_sum else _ZERO

    @property
    def points(self) -> Collection[TradingPoint]:
        return tuple(self._points)
