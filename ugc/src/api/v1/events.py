from flask import Blueprint

routers = Blueprint("ugc", __name__, url_prefix="/ugc")


@routers.post("/click_event")
async def post_click_event():
    pass


@routers.post("/player_event")
async def post_player_event():
    pass
