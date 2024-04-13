from http import HTTPStatus

from flask import Blueprint, request, jsonify

from core.constants import TopicNames
from helpers.access import check_access_token
from models.click import ClickEvent
from models.player import PlayerProgress, EventsNames, PlayerSettingEvents
from repositories.mongo_repositorty import get_mongo_repo
from services.click_event import get_click_service, ClickService
from services.player_events import get_player_service, PlayerService

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event", methods=["POST"])
@check_access_token
async def post_click_event(user_info: dict = None):
    """API for post click events, parsing and moving to Kafka ETL"""
    click_service: ClickService = get_click_service()
    request_data = request.args.to_dict()
    data_model = ClickEvent(**request_data)
    await click_service.send_message(topic_name=TopicNames.click_events, message_model=data_model)
    return jsonify({'message': f'Message sent'}), HTTPStatus.OK


@routers.route("/player_event", methods=["POST"])
@check_access_token
async def post_player_event(user_info: dict = None):
    """API for post player events, parsing and moving to Kafka ETL"""
    player_service: PlayerService = get_player_service()
    request_data = request.args.to_dict()
    request_data["event_type"] = EventsNames[request_data.get("event_type", "")]
    data_model = PlayerSettingEvents(**request_data)
    await player_service.send_message(topic_name=TopicNames.player_settings_events, message_model=data_model)
    return jsonify({'message': f'Message sent'}), HTTPStatus.OK


@routers.route("/player_progress", methods=["POST"])
@check_access_token
async def post_player_progress(user_info: dict = None):
    """API for post player events, parsing and moving to Kafka ETL"""
    player_service: PlayerService = get_player_service()
    request_data = request.args.to_dict()
    data_model = PlayerProgress(**request_data)
    await player_service.send_message(topic_name=TopicNames.player_progress, message_model=data_model)
    return jsonify({'message': f'Message sent'}), HTTPStatus.OK


# TODO: Add check_access_token
@routers.route("/add_bookmark", methods=["POST"])
async def post_add_bookmark():
    request_data = request.args.to_dict()
    # TODO: add bookmark service
    mongo_repo = get_mongo_repo("bookmark")
    await mongo_repo.create(request_data)
    return jsonify({'message': f'Document posted'}), HTTPStatus.OK


@routers.route("/delete_bookmark", methods=["DELETE"])
async def delete_bookmark():
    request_data = request.args.to_dict()
    mongo_repo = get_mongo_repo("bookmark")
    await mongo_repo.delete(request_data)
    return jsonify({'message': f'Document deleted'}), HTTPStatus.OK


@routers.route("/get_bookmark", methods=["GET"])
async def get_bookmark():
    request_data = request.args.to_dict()
    mongo_repo = get_mongo_repo("bookmark")
    response = await mongo_repo.read({"user_id": request_data['user_id']})
    return jsonify(str(response)), HTTPStatus.OK


@routers.route("/add_review", methods=["POST"])
async def add_review():
    request_data = request.args.to_dict()
    mongo_repo = get_mongo_repo("review")
    await mongo_repo.create(request_data)
    return jsonify({'message': f'Document posted'}), HTTPStatus.OK


@routers.route("/update_review", methods=["POST"])
async def update_review():
    request_data = request.args.to_dict()
    mongo_repo = get_mongo_repo("review")
    await mongo_repo.update(
        filter_data={
            "user_id": request_data["user_id"],
            "review_id": request_data["review_id"],
        },
        update_data={"score": request_data["score"]}
    )
    return jsonify({'message': f'Document posted'}), HTTPStatus.OK
