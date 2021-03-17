from logging import getLogger
from typing import Optional, Type

import marshmallow
from marshmallow import Schema, EXCLUDE, post_load, fields
from marshmallow.validate import OneOf

from src.app.coinbase.model import Match, Message, Subscribe
from src.app.errors import SchemaValidationError
from src.app.model import TradingPair

logger = getLogger(__name__)


class SubscribeSchema(Schema):
    type = fields.Constant('subscribe')
    product_ids = fields.List(fields.String())
    channels = fields.List(fields.String())


class MatchSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    size = fields.Decimal(required=True, allow_none=False)
    price = fields.Decimal(required=True, allow_none=False)
    product_id = fields.String(required=True, allow_none=False, validate=OneOf(TradingPair.values()))
    sequence = fields.Integer(required=True, allow_none=False)
    time = fields.DateTime(required=True, allow_none=False, format='iso')

    @post_load
    def build_object(self, data, **_) -> Match:
        product_id = TradingPair(data.pop('product_id'))
        return Match(product_id=product_id, **data)


def deserialize_message(payload: dict) -> Optional[Message]:
    message_type = payload.get('type')
    if not message_type:
        logger.warning(f'Ignoring message without "type" => {payload}')
        return None

    if message_type in ('match', 'last_match'):
        return _deserialize(MatchSchema, payload)

    logger.info(f'Ignoring message with type "{message_type}"')
    return None


def serialize_message(message: Message) -> dict:
    if isinstance(message, Subscribe):
        return _serialize(SubscribeSchema, message)
    raise Exception(f'Message with type "{type(message).__name__}" cannot be serialized')


def _serialize(schema: Type[Schema], message: Message) -> dict:
    return schema().dump(message)


def _deserialize(schema: Type[Schema], payload: dict) -> Message:
    try:
        return schema().load(payload)
    except marshmallow.exceptions.ValidationError as e:
        raise SchemaValidationError('Invalid message payload', failures=e.normalized_messages())
