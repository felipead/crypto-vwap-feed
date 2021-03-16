from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Message(ABC):
    pass


@dataclass
class Match(Message):
    size: Decimal
    price: Decimal
    product_id: str
    sequence: int
    time: datetime
