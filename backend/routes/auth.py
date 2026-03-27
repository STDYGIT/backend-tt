import random
import jwt
import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

REGISTRATION_JWT_SECRET = os.getenv("JWT_SECRET_KEY", "reg-secret-123")


def _generate_otp():
    return str(random.randint(100000, 999999))


def _create_reg_token(payload, expires_minutes=10):
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, REGISTRATION_JWT_SECRET, algorithm="HS256")


def _decode_reg_token(token):
    try:
        return jwt.decode(token, REGISTRATION_JWT_SECRET, algorithms=["HS256"])
    except:
        return None


# ─── Register Flow (Stateless) ────────────────────────────────────────────────

@auth_bp.route("/request-otp", methods=["POST"])
def request_otp():
    """Step 1: Send OTP and return a signed otp_token."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    if not email or "@" not in email:
        return jsonify({"error": "Valid email address required"}), 400

    # Ensure user doesn't already exist with a password
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.password_hash:
        return jsonify({"error": "Account already exists with this email. Please login."}), 409

    otp = _generate_otp()
    
    # Send via Flask-Mail (sync)
    from utils.mail import send_otp_email
    sent = send_otp_email(email, otp)

    # Instead of DB, we return a signed token containing the OTP
    otp_token = _create_reg_token({"email": email, "otp": otp})

    response = {
        "message": "OTP sent successfully",
        "otp_token": otp_token,
    }
    
    if not sent:
        # Debug/fallback for development
        response["debug_otp"] = otp
        response["warning"] = "Email delivery failed. OTP is in the 'debug_otp' field."

    return jsonify(response), 200


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    """Step 2: Verify OTP using the signed otp_token."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    otp = data.get("otp", "").strip()
    otp_token = data.get("otp_token", "")

    if not otp_token:
        return jsonify({"error": "Missing verification token"}), 400

    payload = _decode_reg_token(otp_token)
    if not payload:
        return jsonify({"error": "Invalid or expired verification session"}), 401
    
    if payload.get("email") != email:
        return jsonify({"error": "Incorrect email for this verification session"}), 401
    
    if payload.get("otp") != otp:
        return jsonify({"error": "Correct OTP required"}), 401

    # Return a "verified" token to allow setting password
    verified_token = _create_reg_token({"email": email, "verified": True}, expires_minutes=15)
    
    return jsonify({
        "message": "OTP verified",
        "verified_token": verified_token
    }), 200


@auth_bp.route("/register-final", methods=["POST"])
def register_final():
    """Step 3: Create the user record once name/password are confirmed."""
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    name = data.get("name", "").strip()
    password = data.get("password", "")
    verified_token = data.get("verified_token", "")

    if not verified_token:
        return jsonify({"error": "Verification required"}), 400
    if not name or not password:
        return jsonify({"error": "Name and password required"}), 400

    # Verify the token
    payload = _decode_reg_token(verified_token)
    if not payload or payload.get("email") != email or not payload.get("verified"):
        return jsonify({"error": "Invalid registration session"}), 401

    # Finally, touch the database
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
    
    user.name = name
    user.set_password(password)
    user.is_verified = True
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
        "message": "Account created successfully",
    }), 201


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

    if not user.password_hash:
        return jsonify({"error": "Account exists but registration was never completed. Please register again."}), 403

    if not user.check_password(password):
        return jsonify({"error": "Invalid password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
    }), 200
