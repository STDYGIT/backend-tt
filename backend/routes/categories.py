from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.category import WasteCategory, WasteSubtype

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@categories_bp.route("/", methods=["GET"])
@jwt_required()
def list_categories():
    cats = WasteCategory.query.filter_by(is_active=True).all()
    return jsonify([c.to_dict() for c in cats]), 200
