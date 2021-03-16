import logging
from decimal import Decimal

import dateutil.parser
import pytest

from src.app.coinbase.schema import deserialize_message
from src.app.errors import SchemaValidationError
from src.app.model import Match


def build_match_message() -> dict:
    return {
        'type': 'match',
        'trade_id': 145515540,
        'maker_order_id': '9e1ce308-87c2-4fd5-8424-82458ae68cdc',
        'taker_order_id': '4d121bb6-ae2a-4556-8aa9-2b08964810f7',
        'side': 'sell',
        'size': '0.0245',
        'price': '55868.06',
        'product_id': 'BTC-USD',
        'sequence': 22759566651,
        'time': '2021-03-16T00:10:50.667352Z'
    }


def test_deserialize_valid_match_message():
    payload = build_match_message()

    message = deserialize_message(payload)
    assert message is not None
    assert isinstance(message, Match)

    assert message.size == Decimal(payload['size'])
    assert message.price == Decimal(payload['price'])
    assert message.product_id == payload['product_id']
    assert message.sequence == payload['sequence']
    assert message.time == dateutil.parser.parse(payload['time'])


def test_fail_to_deserialize_match_message_without_size():
    payload = build_match_message()
    del payload['size']

    with pytest.raises(SchemaValidationError) as e:
        deserialize_message(payload)

    assert "{'size': ['Missing data for required field.']}" in str(e.value)


def test_fail_to_deserialize_match_message_without_price():
    payload = build_match_message()
    payload['price'] = None

    with pytest.raises(SchemaValidationError) as e:
        deserialize_message(payload)

    assert "{'price': ['Field may not be null.']}" in str(e.value)


def test_fail_to_deserialize_match_message_without_product_id():
    payload = build_match_message()
    del payload['product_id']

    with pytest.raises(SchemaValidationError) as e:
        deserialize_message(payload)

    assert "{'product_id': ['Missing data for required field.']}" in str(e.value)


def test_fail_to_deserialize_match_message_without_sequence():
    payload = build_match_message()
    del payload['sequence']

    with pytest.raises(SchemaValidationError) as e:
        deserialize_message(payload)

    assert "{'sequence': ['Missing data for required field.']}" in str(e.value)


def test_fail_to_deserialize_match_message_without_time():
    payload = build_match_message()
    payload['time'] = None

    with pytest.raises(SchemaValidationError) as e:
        deserialize_message(payload)

    assert "{'time': ['Field may not be null.']}" in str(e.value)


def test_ignore_subscriptions_message(caplog):
    payload = {
        'type': 'subscriptions',
        'channels': [
            {
                'name': 'matches',
                'product_ids': [
                    'ETH-BTC',
                    'BTC-USD',
                    'ETH-USD'
                ]
            }
        ]
    }

    with caplog.at_level(logging.INFO):
        assert deserialize_message(payload) is None

    assert caplog.records[0].message == 'Ignoring message with type "subscriptions"'


def test_ignore_last_match_message(caplog):
    payload = {
        'type': 'last_match',
        'trade_id': 14569912,
        'maker_order_id': '6389b482-fb57-43ea-8f00-c69dd9bdc162',
        'taker_order_id': '432cd1de-c12f-46df-8088-9f93908a0c1c',
        'side': 'buy',
        'size': '0.00556364',
        'price': '0.03218',
        'product_id': 'ETH-BTC',
        'sequence': 3041220340,
        'time': '2021-03-16T00:10:49.709823Z'
    }

    with caplog.at_level(logging.INFO):
        assert deserialize_message(payload) is None

    assert caplog.records[0].message == 'Ignoring message with type "last_match"'


def test_ignore_message_without_type(caplog):
    payload = {'something': 'evil'}

    with caplog.at_level(logging.WARNING):
        assert deserialize_message(payload) is None

    assert 'Ignoring message without "type"' in caplog.records[0].message
