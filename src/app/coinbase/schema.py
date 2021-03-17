from logging import getLogger
from typing import Optional, Type

import marshmallow
from marshmallow import Schema, EXCLUDE, post_load, fields

from src.app.coinbase.model import Match, Message
from src.app.errors import SchemaValidationError

logger = getLogger(__name__)


class MatchSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    size = fields.Decimal(required=True, allow_none=False)
    price = fields.Decimal(required=True, allow_none=False)
    product_id = fields.String(required=True, allow_none=False)
    sequence = fields.Integer(required=True, allow_none=False)
    time = fields.DateTime(required=True, allow_none=False, format='iso')

    @post_load
    def build_object(self, data, **_) -> Match:
        return Match(**data)


def deserialize_message(payload: dict) -> Optional[Message]:
    message_type = payload.get('type')
    if not message_type:
        logger.warning(f'Ignoring message without "type" => {payload}')
        return None

    # TODO: figure out the difference between "match" and "last_match" message types.
    if message_type == 'match':
        return _deserialize(MatchSchema, payload)

    logger.info(f'Ignoring message with type "{message_type}"')
    return None


def _deserialize(schema: Type[Schema], payload: dict) -> Message:
    try:
        return schema().load(payload)
    except marshmallow.exceptions.ValidationError as e:
        raise SchemaValidationError('Invalid message payload', failures=e.normalized_messages())
