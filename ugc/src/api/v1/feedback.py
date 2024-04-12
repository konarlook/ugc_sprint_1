from flask import Blueprint

from helpers.access import check_access_token

router = Blueprint("ugc", __name__, url_prefix="/ugc")


@router.route("/add_review", methods=["POST"])
@check_access_token
async def port_review(user_info: dict = None):
    """API for post user review on film-work."""
    pass
