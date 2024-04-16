from http import HTTPStatus

from fast_depends import Depends, inject
from flask import Blueprint, jsonify, request
from helpers.access import check_access_token
from models.mongo import collections
from services.likes.likes import LikeService, get_like_service

router = Blueprint("likes", __name__, url_prefix="/ugc")


@router.route("/like", methods=["POST"])
@inject
@check_access_token
async def add_review_like(
    user_info: dict = None,
    like_service: LikeService = Depends(get_like_service),
):
    """API for adding a like to a review."""
    request_data: dict = request.json
    new_like_data = {
        "user_id": user_info.get("sub"),
        "movie_id": str(request_data.get("movie_id")),
        "review_id": str(request_data.get("review_id")),
        "new_value": request_data.get("new_value"),
    }
    new_like = collections.Like(**new_like_data)
    await like_service.create(document=new_like.dict())
    return jsonify({"message": "Like added successfully"}), HTTPStatus.OK


@router.route("/like", methods=["DELETE"])
@inject
@check_access_token
async def remove_review_like(
    user_info: dict = None,
    like_service: LikeService = Depends(get_like_service),
):
    """API for removing a like from a review."""
    request_data: dict = request.json
    await like_service.delete_one(
        filter_data={
            "user_id": user_info.get("sub"),
            "movie_id": str(request_data.get("movie_id")),
            "review_id": str(request_data.get("review_id")),
        }
    )
    return jsonify({"message": "Like removed successfully"}), HTTPStatus.OK
