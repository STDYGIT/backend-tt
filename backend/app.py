import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from extensions import db, jwt, mail
from routes.auth import auth_bp
from routes.user import user_bp
from routes.categories import categories_bp
from routes.entries import entries_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(entries_bp)
    app.register_blueprint(admin_bp)

    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.route("/api/health")
    def health():
        return {"status": "ok", "app": "TrashTreasure"}

    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    """Ensure admin account exists with a default password."""
    from models.user import User
    admin = User.query.filter_by(email="admin@trashtreasure.com").first()
    if not admin:
        admin = User(
            email="admin@trashtreasure.com",
            name="Admin",
            role="admin",
            is_verified=True,
        )
        admin.set_password("Admin@123")
        db.session.add(admin)
        db.session.commit()
        print("[Seed] Admin account created: admin@trashtreasure.com / Admin@123")
    elif not admin.password_hash:
        # Existing admin without password — set it
        admin.is_verified = True
        admin.set_password("Admin@123")
        db.session.commit()
        print("[Seed] Admin password initialized: Admin@123")


app = create_app()
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5001)
