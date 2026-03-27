import random
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _generate_otp():
    return str(random.randint(100000, 999999))


# ─── Register Flow ────────────────────────────────────────────────────────────

@auth_bp.route("/request-otp", methods=["POST"])
def request_otp():
    """Step 1 of registration: send OTP via email."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    if not email or "@" not in email:
        return jsonify({"error": "Valid email address required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)

    otp = _generate_otp()
    user.otp = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    # Send via Flask-Mail (sync)
    from utils.mail import send_otp_email
    sent = send_otp_email(email, otp)

    response = {"message": "OTP sent successfully"}
    if not sent:
        # Fall back: return OTP in response for development/testing
        response["debug_otp"] = otp
        response["warning"] = "Email not configured — OTP shown for development only"

    return jsonify(response), 200


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    """Step 2 of registration: verify OTP, return token + needs_password flag."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    otp = data.get("otp", "").strip()

    if not email or not otp:
        return jsonify({"error": "Email and OTP required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.otp != otp:
        return jsonify({"error": "Invalid OTP"}), 401

    if user.otp_expiry and datetime.utcnow() > user.otp_expiry:
        return jsonify({"error": "OTP expired"}), 401

    user.otp = None
    user.otp_expiry = None
    user.is_verified = True
    db.session.commit()

    needs_password = not bool(user.password_hash)

    # Issue a short-lived token for the set-password step (or full token if already has password)
    token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
        "needs_password": needs_password,
    }), 200


@auth_bp.route("/set-password", methods=["POST"])
def set_password():
    """Step 3 of registration: set password after OTP verification."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    confirm = data.get("confirm_password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    if password != confirm:
        return jsonify({"error": "Passwords do not match"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not user.is_verified:
        return jsonify({"error": "Email not verified. Please verify OTP first"}), 403

    user.set_password(password)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
        "message": "Password set successfully",
    }), 200


# ─── Login ────────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["POST"])
def login():
    """Email + password login."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "No account found. Please register first"}), 404

    if not user.is_verified:
        return jsonify({"error": "Email not verified. Please complete registration"}), 403

    if not user.check_password(password):
        return jsonify({"error": "Invalid password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
    }), 200
