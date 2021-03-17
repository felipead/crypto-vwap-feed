from abc import ABC
from datetime import datetime
from decimal import Decimal

from src.app.model import TradingPoint, TradingPair


class Message(ABC):
    pass


class Match(Message, TradingPoint):

    def __init__(self, size: Decimal, price: Decimal, product_id: str, sequence: int, time: datetime):
        self._size = size
        self._price = price
        self._product_id = product_id
        self._sequence = sequence
        self._time = time

    @property
    def price(self) -> Decimal:
        return self._price

    @property
    def quantity(self) -> Decimal:
        return self._size

    @property
    def sequence(self) -> int:
        return self._sequence

    @property
    def pair(self) -> TradingPair:
        return TradingPair(self._product_id)

    @property
    def time(self) -> datetime:
        return self._time
