from flask import Blueprint

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.route("/click_event", methods=["POST"])
async def post_click_event(username: str):
    return f"User - {username}"


@routers.route("/player_event", methods=["POST"])
async def post_player_event(click: str):
    return f"Click - {click}"
