from http import HTTPStatus
from flask import Blueprint

from helpers.access import check_access_token
from uuid import UUID
import datetime
from flask import request
from models.player import PlayerProgress, EventsNames
from services.player_events import get_player_service, PlayerService

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event/<event_type>", methods=["POST"])
# @check_access_token
async def post_click_event():
    """API for post click events, parsing and moving to Kafka ETL"""
    return [HTTPStatus.OK]


@routers.route("/player_event", methods=["POST"])
# @check_access_token
async def post_player_event():
    """API for post player events, parsing and moving to Kafka ETL"""
    player_service: PlayerService = get_player_service()
    request_data = request.args.to_dict()
    a = EventsNames

    return [HTTPStatus.OK]


@routers.route("/player_progress", methods=["POST"])
# @check_access_token
async def post_player_progress():
    """API for post player events, parsing and moving to Kafka ETL"""
    player_service: PlayerService = get_player_service()
    request_data = request.args.to_dict()
    data_model = PlayerProgress(**request_data)
    await player_service.send_message(topic_name="player_progress", message_model=data_model)
    return [HTTPStatus.OK]
