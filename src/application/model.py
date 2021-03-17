from abc import ABC, abstractmethod
from decimal import Decimal
from functools import total_ordering

from application.enum import TextEnum


class TradingPair(TextEnum):
    BTC_USD = 'BTC-USD'
    ETH_USD = 'ETH-USD'
    ETH_BTC = 'ETH-BTC'


@total_ordering
class TradingPoint(ABC):

    @property
    @abstractmethod
    def pair(self) -> TradingPair:
        pass

    @property
    @abstractmethod
    def quantity(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def price(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def sequence(self) -> int:
        pass

    def __lt__(self, other: 'TradingPoint') -> bool:
        return self.sequence < other.sequence
