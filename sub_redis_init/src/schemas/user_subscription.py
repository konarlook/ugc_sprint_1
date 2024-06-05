from uuid import UUID

from .base import BaseSchema
from pydantic import field_validator


class UserSubscriptionSchema(BaseSchema):
    user_id: str
    subscription_id: str
    time: int

    @field_validator('user_id')
    def validate_user_id_as_uuid(cls, value, info):
        try:
            uuid_obj = UUID(value, version=4)
            return value
        except Exception as e:
            raise e

    @field_validator('subscription_id')
    def validate_subscription_id_as_uuid(cls, value, info):
        try:
            uuid_obj = UUID(value, version=4)
            return value
        except Exception as e:
            raise e
