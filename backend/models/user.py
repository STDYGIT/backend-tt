from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default="user")  # 'user' or 'admin'
    password_hash = db.Column(db.String(256), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    otp = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    entries = db.relationship("WasteEntry", backref="user", lazy=True, cascade="all, delete-orphan", foreign_keys="WasteEntry.user_id")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def total_earnings(self):
        """Sum of prices from completed entries."""
        from models.entry import WasteEntry
        completed = WasteEntry.query.filter_by(
            user_id=self.id, status=WasteEntry.STATUS_COMPLETED
        ).all()
        return sum((e.price or 0) for e in completed)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_verified": self.is_verified,
            "total_earnings": self.total_earnings,
            "created_at": self.created_at.isoformat(),
        }
