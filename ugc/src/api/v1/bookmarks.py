import json
from http import HTTPStatus

from beanie import Document
from flask import Blueprint, request, jsonify, Response
from fast_depends import inject, Depends

from helpers.access import check_access_token
from models.mongo import collections
from services.bookmarks import get_bookmark_service, BookmarkService
from services.feedback.review import ReviewService, get_review_service

router = Blueprint("bookmark", __name__, url_prefix="/ugc")


@router.route("/bookmark", methods=["POST"])
@inject
@check_access_token
async def post_bookmark(
        user_info: dict = None,
        review_service: BookmarkService = Depends(get_bookmark_service),
):
    request_data: dict = request.args.to_dict()
    request_data["user_id"] = user_info.get("sub")
    review: Document = collections.Bookmark(**request_data)
    await review_service.save_bookmark(
        document=review.dict(),
    )
    return jsonify({"message": "Successful writing"}), HTTPStatus.OK


@router.route("/bookmark", methods=["DELETE"])
@inject
@check_access_token
async def delete_bookmark(
        user_info: dict = None,
        review_service: BookmarkService = Depends(get_bookmark_service),
):
    request_data: dict = request.args.to_dict()
    request_data["user_id"] = user_info.get("sub")
    review: Document = collections.Bookmark(**request_data)
    await review_service.delete_bookmark(
        document=review.dict(),
    )
    return jsonify({"message": "Successful deleting"}), HTTPStatus.OK
