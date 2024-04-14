from http import HTTPStatus
from flask import Blueprint, request, jsonify
from fast_depends import inject, Depends

from helpers.access import check_access_token
from services.review import ReviewService, get_review_service

router = Blueprint("feedback", __name__, url_prefix="/ugc")


@router.route("/review", methods=["POST"])
@inject
@check_access_token
async def post_review(
    user_info: dict = None,
    review_service: ReviewService = Depends(get_review_service),
):
    """API for post user review on film-work."""
    request_data: dict = request.args.to_dict()
    review_service.create(document=request_data)
    return jsonify({"message": "Successful writing"}), HTTPStatus.OK


@router.route("/review", methods=["GET"])
@inject
@check_access_token
async def get_reviews(
    user_info: dict = None,
    review_service: ReviewService = Depends(get_review_service),
):
    """API for getting all reviews on film-work."""
    pass


@router.route("/review", methods=["DELETE"])
@inject
@check_access_token
async def delete_review(
    user_info: dict = None,
    review_service: ReviewService = Depends(get_review_service),
):
    """Delete self review on film-work."""
    pass


@router.route("/review", methods=["UPDATE"])
@inject
@check_access_token
async def update_review(
    user_info: dict = None,
    review_service: ReviewService = Depends(get_review_service),
):
    """Update self review on film-work."""
    pass
