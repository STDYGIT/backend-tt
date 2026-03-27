from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.entry import WasteEntry
from models.category import WasteCategory, WasteSubtype
from models.pickup import PickupZone, PickupSlot

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def require_admin():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return None, (jsonify({"error": "Admin access required"}), 403)
    return user, None


# ─── Dashboard ────────────────────────────────────────────────────────────────

@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    _, err = require_admin()
    if err:
        return err

    total = WasteEntry.query.count()
    pending = WasteEntry.query.filter_by(status=WasteEntry.STATUS_PENDING).count()
    under_verification = WasteEntry.query.filter_by(status=WasteEntry.STATUS_UNDER_VERIFICATION).count()
    verified = WasteEntry.query.filter_by(status=WasteEntry.STATUS_VERIFIED).count()
    scheduled = WasteEntry.query.filter_by(status=WasteEntry.STATUS_SCHEDULED).count()
    completed = WasteEntry.query.filter_by(status=WasteEntry.STATUS_COMPLETED).count()
    rejected = WasteEntry.query.filter_by(status=WasteEntry.STATUS_REJECTED).count()
    total_users = User.query.filter_by(role="user").count()

    # Total earnings: sum of prices from completed entries
    completed_entries = WasteEntry.query.filter_by(status=WasteEntry.STATUS_COMPLETED).all()
    total_earnings = sum((e.price or 0) for e in completed_entries)

    return jsonify({
        "total_entries": total,
        "total_users": total_users,
        "pending": pending,
        "under_verification": under_verification,
        "verified": verified,
        "scheduled": scheduled,
        "completed": completed,
        "rejected": rejected,
        "total_earnings": total_earnings,
    }), 200


# ─── User Management ──────────────────────────────────────────────────────────

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    _, err = require_admin()
    if err:
        return err

    users = User.query.order_by(User.created_at.desc()).all()
    result = []
    for u in users:
        ud = u.to_dict()
        if u.role == "admin":
            ud["reviewed_count"] = WasteEntry.query.filter_by(reviewed_by_id=u.id).count()
        else:
            ud["entries_count"] = WasteEntry.query.filter_by(user_id=u.id).count()
            # calculate earnings only for normal users
            completed_entries = WasteEntry.query.filter_by(user_id=u.id, status=WasteEntry.STATUS_COMPLETED).all()
            ud["total_earnings"] = sum((e.price or 0) for e in completed_entries)
        result.append(ud)
    return jsonify(result), 200


@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    _, err = require_admin()
    if err:
        return err

    user = User.query.get_or_404(user_id)
    ud = user.to_dict()
    if user.role == "admin":
        ud["reviewed_entries"] = [e.to_dict() for e in WasteEntry.query.filter_by(reviewed_by_id=user_id).order_by(WasteEntry.updated_at.desc()).all()]
    else:
        ud["entries"] = [e.to_dict() for e in WasteEntry.query.filter_by(user_id=user_id).order_by(WasteEntry.created_at.desc()).all()]
    return jsonify(ud), 200


@admin_bp.route("/users/<int:user_id>/promote", methods=["PUT"])
@jwt_required()
def promote_user(user_id):
    admin, err = require_admin()
    if err:
        return err
    if admin.id == user_id:
        return jsonify({"error": "Cannot change your own role"}), 400

    user = User.query.get_or_404(user_id)
    user.role = "admin" if user.role == "user" else "user"
    db.session.commit()
    return jsonify({"message": f"Role updated to {user.role}", "user": user.to_dict()}), 200


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    admin, err = require_admin()
    if err:
        return err
    if admin.id == user_id:
        return jsonify({"error": "Cannot delete yourself"}), 400

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


# ─── Entries ──────────────────────────────────────────────────────────────────

@admin_bp.route("/entries", methods=["GET"])
@jwt_required()
def list_entries():
    _, err = require_admin()
    if err:
        return err

    status_filter = request.args.get("status")
    query = WasteEntry.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    entries = query.order_by(WasteEntry.created_at.desc()).all()
    return jsonify([e.to_dict() for e in entries]), 200


@admin_bp.route("/entries/<int:entry_id>/status", methods=["PUT"])
@jwt_required()
def update_entry_status(entry_id):
    admin, err = require_admin()
    if err:
        return err

    entry = WasteEntry.query.get_or_404(entry_id)
    data = request.get_json()
    new_status = data.get("status")
    admin_notes = data.get("admin_notes")

    valid_statuses = [
        WasteEntry.STATUS_UNDER_VERIFICATION,
        WasteEntry.STATUS_VERIFIED,
        WasteEntry.STATUS_LOCATION_REQUIRED,
        WasteEntry.STATUS_CONFIRMED,
        WasteEntry.STATUS_SCHEDULED,
        WasteEntry.STATUS_COMPLETED,
        WasteEntry.STATUS_REJECTED,
    ]
    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status: {new_status}"}), 400

    entry.status = new_status
    if admin_notes is not None:
        entry.admin_notes = admin_notes

    # Handle pricing (admin can set price when updating status)
    if "price" in data and data["price"] is not None:
        entry.price = float(data["price"])
    if "price_type" in data and data["price_type"] is not None:
        entry.price_type = data["price_type"]

    entry.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(entry.to_dict()), 200


# ─── Categories ───────────────────────────────────────────────────────────────

@admin_bp.route("/categories", methods=["GET"])
@jwt_required()
def list_categories():
    _, err = require_admin()
    if err:
        return err
    cats = WasteCategory.query.all()
    return jsonify([c.to_dict() for c in cats]), 200


@admin_bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():
    _, err = require_admin()
    if err:
        return err
    data = request.get_json()
    cat = WasteCategory(
        name=data["name"],
        icon=data.get("icon", "♻️"),
        color=data.get("color", "#4CAF71"),
    )
    db.session.add(cat)
    db.session.commit()
    return jsonify(cat.to_dict()), 201


@admin_bp.route("/categories/<int:cat_id>", methods=["PUT"])
@jwt_required()
def update_category(cat_id):
    _, err = require_admin()
    if err:
        return err
    cat = WasteCategory.query.get_or_404(cat_id)
    data = request.get_json()
    cat.name = data.get("name", cat.name)
    cat.icon = data.get("icon", cat.icon)
    cat.color = data.get("color", cat.color)
    cat.is_active = data.get("is_active", cat.is_active)
    db.session.commit()
    return jsonify(cat.to_dict()), 200


@admin_bp.route("/categories/<int:cat_id>", methods=["DELETE"])
@jwt_required()
def delete_category(cat_id):
    _, err = require_admin()
    if err:
        return err
    cat = WasteCategory.query.get_or_404(cat_id)
    cat.is_active = False
    db.session.commit()
    return jsonify({"message": "Category deactivated"}), 200


@admin_bp.route("/categories/<int:cat_id>/subtypes", methods=["POST"])
@jwt_required()
def create_subtype(cat_id):
    _, err = require_admin()
    if err:
        return err
    WasteCategory.query.get_or_404(cat_id)
    data = request.get_json()
    sub = WasteSubtype(
        category_id=cat_id,
        name=data["name"],
        rate_per_unit=data.get("rate_per_unit", 0.0),
        unit=data.get("unit", "kg")
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify(sub.to_dict()), 201


@admin_bp.route("/subtypes/<int:sub_id>", methods=["PUT"])
@jwt_required()
def update_subtype(sub_id):
    _, err = require_admin()
    if err:
        return err
    sub = WasteSubtype.query.get_or_404(sub_id)
    data = request.get_json()
    sub.name = data.get("name", sub.name)
    sub.is_active = data.get("is_active", sub.is_active)
    if "rate_per_unit" in data:
        sub.rate_per_unit = float(data["rate_per_unit"])
    if "unit" in data:
        sub.unit = data["unit"]
    db.session.commit()
    return jsonify(sub.to_dict()), 200


@admin_bp.route("/subtypes/<int:sub_id>", methods=["DELETE"])
@jwt_required()
def delete_subtype(sub_id):
    _, err = require_admin()
    if err:
        return err
    sub = WasteSubtype.query.get_or_404(sub_id)
    sub.is_active = False
    db.session.commit()
    return jsonify({"message": "Subtype deactivated"}), 200


# ─── Pickup Zones ─────────────────────────────────────────────────────────────

@admin_bp.route("/zones", methods=["GET"])
@jwt_required()
def list_zones():
    _, err = require_admin()
    if err:
        return err
    zones = PickupZone.query.filter_by(is_active=True).all()
    return jsonify([z.to_dict() for z in zones]), 200


@admin_bp.route("/zones", methods=["POST"])
@jwt_required()
def create_zone():
    _, err = require_admin()
    if err:
        return err
    data = request.get_json()
    zone = PickupZone(name=data["name"], description=data.get("description"))
    db.session.add(zone)
    db.session.commit()
    return jsonify(zone.to_dict()), 201


@admin_bp.route("/zones/<int:zone_id>", methods=["PUT"])
@jwt_required()
def update_zone(zone_id):
    _, err = require_admin()
    if err:
        return err
    zone = PickupZone.query.get_or_404(zone_id)
    data = request.get_json()
    zone.name = data.get("name", zone.name)
    zone.description = data.get("description", zone.description)
    zone.is_active = data.get("is_active", zone.is_active)
    db.session.commit()
    return jsonify(zone.to_dict()), 200


# ─── Pickup Slots ─────────────────────────────────────────────────────────────

@admin_bp.route("/slots", methods=["GET"])
@jwt_required()
def list_slots():
    _, err = require_admin()
    if err:
        return err
    slots = PickupSlot.query.order_by(PickupSlot.date, PickupSlot.time_range).all()
    return jsonify([s.to_dict() for s in slots]), 200


@admin_bp.route("/slots", methods=["POST"])
@jwt_required()
def create_slot():
    _, err = require_admin()
    if err:
        return err
    data = request.get_json()
    slot = PickupSlot(
        zone_id=data["zone_id"],
        date=data["date"],
        time_range=data["time_range"],
        capacity=data.get("capacity", 10),
    )
    db.session.add(slot)
    db.session.commit()
    return jsonify(slot.to_dict()), 201


@admin_bp.route("/slots/<int:slot_id>", methods=["DELETE"])
@jwt_required()
def delete_slot(slot_id):
    _, err = require_admin()
    if err:
        return err
    slot = PickupSlot.query.get_or_404(slot_id)
    slot.is_active = False
    db.session.commit()
    return jsonify({"message": "Slot deactivated"}), 200
