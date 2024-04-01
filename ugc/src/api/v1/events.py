from http import HTTPStatus
from flask import Blueprint, jsonify, request
from helpers.access import check_access_token
from models.click import Click

from services.click_event import get_click_service
from flask_jwt_extended import jwt_required, get_jwt_identity

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event/<event_type>", methods=["POST"])
@jwt_required()
# @check_access_token
async def post_click_event(
    # access_token: str,
    event_type: str,
    # url: str = None,
) -> int:
    """API for post click events, parsing and moving to Kafka ETL"""

    user = get_jwt_identity()
    data = request.json
    click = Click(**data, user_id=user)
    click_service = get_click_service()
    await click_service.produce(topicname=event_type, click=click)
    return jsonify({"message": "Click event received and processed"}), HTTPStatus.OK

@routers.route("/player_event/<event_type>", methods=["POST"])
@check_access_token
async def post_player_event(
    access_token: str,
    event_type: str,
    movie_url: str,
) -> int:
    """API for post player events, parsing and moving to Kafka ETL"""
    return HTTPStatus.OK
