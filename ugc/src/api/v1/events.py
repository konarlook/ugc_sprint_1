from http import HTTPStatus
from flask import Blueprint
from flask_pydantic import validate

from helpers.access import check_access_token
from uuid import UUID
import datetime
from flask import request
from models.player import PlayerProgress
from services.player_events import get_player_service

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event/<event_type>", methods=["POST"])
# @check_access_token
async def post_click_event(
        access_token: str,
        event_type: str,
        url: str = None,
) -> int:
    """API for post click events, parsing and moving to Kafka ETL"""
    return HTTPStatus.OK


@routers.route("/player_event/<event_type>", methods=["POST"])
# @check_access_token
async def post_player_event(
        access_token: str,
        event_type: str,
        movie_url: str,
) -> int:
    """API for post player events, parsing and moving to Kafka ETL"""
    return HTTPStatus.OK


@routers.route("/player_progress", methods=["POST"])
# @check_access_token
async def post_player_progress() -> int:
    user_id = request.args.get("user_id")
    movie_id = request.args.get("movie_id")
    event_dt = request.args.get("event_dt")
    view_progress = request.args.get("view_progress")
    movie_duration = request.args.get("movie_duration")
    """API for post player events, parsing and moving to Kafka ETL"""
    player_service = get_player_service()
    data_model = PlayerProgress(
        user_id=user_id,
        movie_id=movie_id,
        event_dt=event_dt,
        view_progress=view_progress,
        movie_duration=movie_duration,
    )
    await player_service.produce(topic_name="player_progress", message_model=data_model)
    return [HTTPStatus.OK]
