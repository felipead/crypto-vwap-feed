from decimal import Decimal
from typing import List

import pytest

from application.model import TradingPair, TradingPoint
from application.vwap import VWAP


class FakePoint(TradingPoint):
    def __init__(self, pair: TradingPair, price: Decimal, quantity: Decimal, sequence: int):
        self._pair = pair
        self._price = price
        self._quantity = quantity
        self._sequence = sequence

    @property
    def pair(self) -> TradingPair:
        return self._pair

    @property
    def quantity(self) -> Decimal:
        return self._quantity

    @property
    def price(self) -> Decimal:
        return self._price

    @property
    def sequence(self) -> int:
        return self._sequence


def sequences(vwap: VWAP) -> List[int]:
    return [i.sequence for i in vwap.points]


def new_point(
        pair: str = 'BTC-USD',
        quantity: str = '0.0245',
        price: str = '55868.06',
        sequence: int = 9876543210
) -> TradingPoint:
    return FakePoint(
        pair=TradingPair(pair),
        quantity=Decimal(quantity),
        price=Decimal(price),
        sequence=sequence,
    )


def test_add_points_ensuring_the_list_remains_sorted_by_sequence():
    vwap = VWAP(TradingPair.BTC_USD)

    vwap.add(new_point(sequence=9999999903))
    vwap.add(new_point(sequence=9999999909))
    vwap.add(new_point(sequence=9999999904))
    vwap.add(new_point(sequence=9999999908))
    vwap.add(new_point(sequence=9999999901))
    vwap.add(new_point(sequence=9999999910))
    vwap.add(new_point(sequence=42))
    vwap.add(new_point(sequence=9999999905))
    vwap.add(new_point(sequence=9999999907))
    vwap.add(new_point(sequence=9999999902))
    vwap.add(new_point(sequence=9999999906))

    assert sequences(vwap) == [
        42,
        9999999901,
        9999999902,
        9999999903,
        9999999904,
        9999999905,
        9999999906,
        9999999907,
        9999999908,
        9999999909,
        9999999910,
    ]


def test_add_points_discarding_the_oldest_when_the_list_grows_more_than_max_size():
    vwap = VWAP(TradingPair.BTC_USD, max_size=20)

    vwap.add(new_point(sequence=1040))
    vwap.add(new_point(sequence=1020))
    vwap.add(new_point(sequence=1030))
    vwap.add(new_point(sequence=1090))
    vwap.add(new_point(sequence=1060))
    vwap.add(new_point(sequence=1010))
    vwap.add(new_point(sequence=1070))
    vwap.add(new_point(sequence=1180))
    vwap.add(new_point(sequence=1080))
    vwap.add(new_point(sequence=1100))
    vwap.add(new_point(sequence=1160))
    vwap.add(new_point(sequence=1150))
    vwap.add(new_point(sequence=1110))
    vwap.add(new_point(sequence=1120))
    vwap.add(new_point(sequence=1130))
    vwap.add(new_point(sequence=1200))
    vwap.add(new_point(sequence=1050))
    vwap.add(new_point(sequence=1140))
    vwap.add(new_point(sequence=1170))
    vwap.add(new_point(sequence=1190))

    assert sequences(vwap) == [
        1010,
        1020,
        1030,
        1040,
        1050,
        1060,
        1070,
        1080,
        1090,
        1100,
        1110,
        1120,
        1130,
        1140,
        1150,
        1160,
        1170,
        1180,
        1190,
        1200,
    ]

    vwap.add(new_point(sequence=1171))
    assert sequences(vwap) == [
        1020,
        1030,
        1040,
        1050,
        1060,
        1070,
        1080,
        1090,
        1100,
        1110,
        1120,
        1130,
        1140,
        1150,
        1160,
        1170,
        1171,  # <== new point added here
        1180,
        1190,
        1200,
    ]

    vwap.add(new_point(sequence=1201))
    assert sequences(vwap) == [
        1030,
        1040,
        1050,
        1060,
        1070,
        1080,
        1090,
        1100,
        1110,
        1120,
        1130,
        1140,
        1150,
        1160,
        1170,
        1171,
        1180,
        1190,
        1200,
        1201,  # <== new point added here
    ]

    vwap.add(new_point(sequence=1031))
    assert sequences(vwap) == [
        1031,  # <== new point added here
        1040,
        1050,
        1060,
        1070,
        1080,
        1090,
        1100,
        1110,
        1120,
        1130,
        1140,
        1150,
        1160,
        1170,
        1171,
        1180,
        1190,
        1200,
        1201,
    ]


def test_do_not_add_point_that_has_a_sequence_smaller_than_the_least_sequence_when_the_list_is_already_full():
    vwap = VWAP(TradingPair.BTC_USD, max_size=10)

    vwap.add(new_point(sequence=3))
    vwap.add(new_point(sequence=10))
    vwap.add(new_point(sequence=4))
    vwap.add(new_point(sequence=6))
    vwap.add(new_point(sequence=2))
    vwap.add(new_point(sequence=11))
    vwap.add(new_point(sequence=8))
    vwap.add(new_point(sequence=9))
    vwap.add(new_point(sequence=5))
    vwap.add(new_point(sequence=7))

    assert sequences(vwap) == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    vwap.add(new_point(sequence=1))

    assert sequences(vwap) == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def test_fail_when_trying_to_add_point_that_does_not_belong_to_the_vwap_trading_pair():
    vwap = VWAP(TradingPair.ETH_BTC)

    with pytest.raises(ValueError) as e:
        vwap.add(new_point(pair='BTC-USD'))

    assert str(e.value) == 'Unsupported trading pair: BTC-USD'


def test_compute_the_current_vwap_value_when_the_list_is_empty():
    vwap = VWAP(TradingPair.BTC_USD)

    assert vwap.current_value() == Decimal(0)


def test_compute_the_current_vwap_value_when_the_list_has_one_point():
    vwap = VWAP(TradingPair.ETH_BTC)

    vwap.add(new_point('ETH-BTC', quantity='0.00015', price='59326.253'))

    assert vwap.current_value() == Decimal('59326.253')


def test_compute_the_current_vwap_value_when_the_list_has_some_points():
    vwap = VWAP(TradingPair.BTC_USD)

    vwap.add(new_point(quantity='1.23400', price='59293.253', sequence=5))
    vwap.add(new_point(quantity='0.09123', price='59398.973', sequence=3))
    vwap.add(new_point(quantity='1.00083', price='59325.001', sequence=1))
    vwap.add(new_point(quantity='0.00015', price='59327.830', sequence=2))
    vwap.add(new_point(quantity='0.89135', price='58725.301', sequence=6))
    vwap.add(new_point(quantity='0.00378', price='59350.030', sequence=4))

    value = vwap.current_value()

    assert value == (
            (
                    (Decimal('1.23400') * Decimal('59293.253')) +
                    (Decimal('0.09123') * Decimal('59398.973')) +
                    (Decimal('1.00083') * Decimal('59325.001')) +
                    (Decimal('0.00015') * Decimal('59327.830')) +
                    (Decimal('0.89135') * Decimal('58725.301')) +
                    (Decimal('0.00378') * Decimal('59350.030'))
            ) / (
                    Decimal('1.23400') +
                    Decimal('0.09123') +
                    Decimal('1.00083') +
                    Decimal('0.00015') +
                    Decimal('0.89135') +
                    Decimal('0.00378')
            )
    )

    assert value == Decimal('59149.02574514642974662717999')


def test_to_string():
    assert str(VWAP(TradingPair.ETH_USD)) == 'VWAP[ETH-USD]'


def test_supports_point_if_trading_pair_is_the_same():
    vwap = VWAP(TradingPair.ETH_USD)
    assert vwap.supports(new_point('ETH-USD')) is True


def test_does_not_support_point_with_different_trading_pair():
    vwap = VWAP(TradingPair.ETH_USD)
    assert vwap.supports(new_point('BTC-USD')) is False
