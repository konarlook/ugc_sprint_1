import functools
from typing import Callable
from datetime import datetime

import jwt

from core.config import settings
from core.exceptions import TokenException, ForbiddenException


async def is_token_expired(token: str, action_name: str) -> bool:
    if not token:
        raise TokenException
    token_info: dict = jwt.decode(
        jwt=token,
        key=settings.auth_jwt.public_key.read_text(),
        algorithms=[
            settings.auth_jwt.auth_algorithm_password,
        ],
    )

    token_expired = datetime.utcfromtimestamp(token_info.get("exp"))
    if token_expired < datetime.utcnow():
        raise TokenException

    user_actions = token_info.get("actions")
    if action_name not in user_actions:
        raise ForbiddenException
    return True


def check_access_token(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        access_token = kwargs.get("access_token")
        await is_token_expired(access_token, action_name=func.__name__)
        return await func(*args, **kwargs)

    return wrapper
