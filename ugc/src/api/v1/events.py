from http import HTTPStatus
from flask import Blueprint
from helpers.access import check_access_token

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event/<event_type>", methods=["POST"])
@check_access_token
async def post_click_event(
    access_token: str,
    event_type: str,
    url: str = None,
) -> int:
    """API for post click events, parsing and moving to Kafka ETL"""
    return HTTPStatus.OK


@routers.route("/player_event/<event_type>", methods=["POST"])
@check_access_token
async def post_player_event(
    access_token: str,
    event_type: str,
    movie_url: str,
) -> int:
    """API for post player events, parsing and moving to Kafka ETL"""
    return HTTPStatus.OK
