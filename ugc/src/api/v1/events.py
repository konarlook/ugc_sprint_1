from flask import Blueprint

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event/<event_type>", methods=["POST"])
async def post_click_event(
    event_type: str, jwt_token: str, event_dt: str, url: str | None
) -> str:
    """API for post click events, parsing and moving to Kafka ETL"""
    return f"User - {event_type}"


@routers.route("/player_event/<event_type>", methods=["POST"])
async def post_player_event(
    event_type: str, jwt_token: str, event_dt: str, movies_url: str
) -> str:
    """API for post player events, parsing and moving to Kafka ETL"""
    return f"Click - {event_type}"
