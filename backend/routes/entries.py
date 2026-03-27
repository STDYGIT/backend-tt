import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.entry import WasteEntry
from models.category import WasteCategory, WasteSubtype
from models.pickup import PickupSlot, PickupAssignment
from utils.image_upload import upload_image

entries_bp = Blueprint("entries", __name__, url_prefix="/api/entries")


@entries_bp.route("/", methods=["POST"])
@jwt_required()
def create_entry():
    user_id = int(get_jwt_identity())
    category_id = request.form.get("category_id")
    subtype_id = request.form.get("subtype_id")
    subtype_other = request.form.get("subtype_other")
    description = request.form.get("description")
    condition = request.form.get("condition")
    age_usage = request.form.get("age_usage")

    if not category_id:
        return jsonify({"error": "Category is required"}), 400

    image_url = None
    if "image" in request.files:
        file = request.files["image"]
        if file.filename:
            cfg = current_app.config
            image_url = upload_image(
                file,
                cfg["UPLOAD_FOLDER"],
                use_cloudinary=cfg["USE_CLOUDINARY"],
                cloudinary_config={
                    "cloud_name": cfg["CLOUDINARY_CLOUD_NAME"],
                    "api_key": cfg["CLOUDINARY_API_KEY"],
                    "api_secret": cfg["CLOUDINARY_API_SECRET"],
                },
            )

    entry = WasteEntry(
        user_id=user_id,
        category_id=int(category_id),
        subtype_id=int(subtype_id) if subtype_id else None,
        subtype_other=subtype_other,
        description=description,
        condition=condition,
        age_usage=age_usage,
        image_url=image_url,
        status=WasteEntry.STATUS_PENDING,
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201


@entries_bp.route("/", methods=["GET"])
@jwt_required()
def list_entries():
    user_id = int(get_jwt_identity())
    entries = WasteEntry.query.filter_by(user_id=user_id).order_by(WasteEntry.created_at.desc()).all()
    return jsonify([e.to_dict() for e in entries]), 200


@entries_bp.route("/<int:entry_id>", methods=["GET"])
@jwt_required()
def get_entry(entry_id):
    user_id = int(get_jwt_identity())
    entry = WasteEntry.query.get_or_404(entry_id)
    user = User.query.get(user_id)
    if entry.user_id != user_id and user.role != "admin":
        return jsonify({"error": "Forbidden"}), 403
    return jsonify(entry.to_dict()), 200


@entries_bp.route("/<int:entry_id>/location", methods=["POST"])
@jwt_required()
def save_location(entry_id):
    user_id = int(get_jwt_identity())
    entry = WasteEntry.query.get_or_404(entry_id)
    if entry.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    if entry.status != WasteEntry.STATUS_LOCATION_REQUIRED:
        return jsonify({"error": "Location not required at this stage"}), 400

    data = request.get_json()
    entry.location_lat = data.get("lat")
    entry.location_lng = data.get("lng")
    entry.location_address = data.get("address")
    entry.status = WasteEntry.STATUS_CONFIRMED
    entry.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(entry.to_dict()), 200


@entries_bp.route("/<int:entry_id>/slots", methods=["GET"])
@jwt_required()
def available_slots(entry_id):
    entry = WasteEntry.query.get_or_404(entry_id)
    slots = PickupSlot.query.filter(
        PickupSlot.is_active == True,
        PickupSlot.booked_count < PickupSlot.capacity,
    ).order_by(PickupSlot.date, PickupSlot.time_range).all()
    return jsonify([s.to_dict() for s in slots]), 200


@entries_bp.route("/<int:entry_id>/schedule", methods=["POST"])
@jwt_required()
def schedule_pickup(entry_id):
    user_id = int(get_jwt_identity())
    entry = WasteEntry.query.get_or_404(entry_id)
    if entry.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    if entry.status != WasteEntry.STATUS_CONFIRMED:
        return jsonify({"error": "Entry must be confirmed before scheduling"}), 400

    data = request.get_json()
    slot_id = data.get("slot_id")
    slot = PickupSlot.query.get_or_404(slot_id)
    if slot.booked_count >= slot.capacity:
        return jsonify({"error": "Slot is full"}), 400

    assignment = PickupAssignment(entry_id=entry_id, slot_id=slot_id)
    slot.booked_count += 1
    entry.status = WasteEntry.STATUS_SCHEDULED
    entry.updated_at = datetime.utcnow()
    db.session.add(assignment)
    db.session.commit()
    return jsonify(entry.to_dict()), 200
