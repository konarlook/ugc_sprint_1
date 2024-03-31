from http import HTTPStatus
from werkzeug.exceptions import HTTPException


class TokenException(HTTPException):
    code = HTTPStatus.UNAUTHORIZED
    description = "Incorrect access token."


class ForbiddenException(HTTPException):
    code = HTTPStatus.FORBIDDEN
    description = "Insufficient privileges to use this function."
