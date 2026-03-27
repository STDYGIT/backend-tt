from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.entry import WasteEntry

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = user.to_dict()
    # Include detailed earnings breakdown
    completed_entries = WasteEntry.query.filter_by(
        user_id=user_id, status=WasteEntry.STATUS_COMPLETED
    ).all()
    data["earnings_breakdown"] = [
        {"entry_id": e.id, "price": e.price, "price_type": e.price_type,
         "category": e.category.name if e.category else None}
        for e in completed_entries if e.price
    ]
    return jsonify(data), 200


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if "name" in data:
        user.name = data["name"].strip()
    db.session.commit()
    return jsonify(user.to_dict()), 200
