from http import HTTPStatus

from flask import Blueprint
from flask import request, jsonify

from core.constants import TopicNames
from models.click import ClickEvent
from models.player import PlayerProgress, EventsNames, PlayerSettingEvents
from services.click_event import get_click_service, ClickService
from services.player_events import get_player_service, PlayerService

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event", methods=["POST"])
# @check_access_token
async def post_click_event():
    """API for post click events, parsing and moving to Kafka ETL"""
    click_service: ClickService = get_click_service()
    request_data = request.args.to_dict()
    data_model = ClickEvent(**request_data)
    await click_service.send_message(topic_name=TopicNames.click_events, message_model=data_model)
    return jsonify({'message': f'Message sent'}), HTTPStatus.OK


@routers.route("/player_event", methods=["POST"])
# @check_access_token
async def post_player_event():
    """API for post player events, parsing and moving to Kafka ETL"""
    player_service: PlayerService = get_player_service()
    request_data = request.args.to_dict()
    request_data["event_type"] = EventsNames[request_data["event_type"]]
    data_model = PlayerSettingEvents(**request_data)
    await player_service.send_message(topic_name=TopicNames.player_settings_events, message_model=data_model)
    return jsonify({'message': f'Message sent'}), HTTPStatus.OK


@routers.route("/player_progress", methods=["POST"])
# @check_access_token
async def post_player_progress():
    """API for post player events, parsing and moving to Kafka ETL"""
    player_service: PlayerService = get_player_service()
    request_data = request.args.to_dict()
    data_model = PlayerProgress(**request_data)
    await player_service.send_message(topic_name=TopicNames.player_progress, message_model=data_model)
    return jsonify({'message': f'Message sent'}), HTTPStatus.OK
