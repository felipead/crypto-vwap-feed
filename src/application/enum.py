from enum import Enum
from typing import Collection


class TextEnum(Enum):
    @classmethod
    def values(cls) -> Collection[str]:
        return tuple(i.value for i in cls)

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)
