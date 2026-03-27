from datetime import datetime
from extensions import db


class WasteEntry(db.Model):
    __tablename__ = "waste_entries"

    # Status constants
    STATUS_PENDING = "pending"
    STATUS_UNDER_VERIFICATION = "under_verification"
    STATUS_VERIFIED = "verified"
    STATUS_LOCATION_REQUIRED = "location_required"
    STATUS_CONFIRMED = "confirmed"
    STATUS_SCHEDULED = "scheduled"
    STATUS_COMPLETED = "completed"
    STATUS_REJECTED = "rejected"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("waste_categories.id"), nullable=False)
    subtype_id = db.Column(db.Integer, db.ForeignKey("waste_subtypes.id"), nullable=True)
    subtype_other = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    condition = db.Column(db.String(100), nullable=True)
    age_usage = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default=STATUS_PENDING)
    admin_notes = db.Column(db.Text, nullable=True)
    # Pricing (set by admin)
    price = db.Column(db.Float, nullable=True)
    price_type = db.Column(db.String(20), nullable=True)  # 'per_item' or 'per_image'
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    location_lat = db.Column(db.Float, nullable=True)
    location_lng = db.Column(db.Float, nullable=True)
    location_address = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship("WasteCategory", backref="entries")
    subtype = db.relationship("WasteSubtype", backref="entries")
    pickup_assignment = db.relationship("PickupAssignment", backref="entry", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else None,
            "user_email": self.user.email if self.user else None,
            "category": self.category.to_dict(include_subtypes=False) if self.category else None,
            "subtype": self.subtype.to_dict() if self.subtype else None,
            "subtype_other": self.subtype_other,
            "description": self.description,
            "condition": self.condition,
            "age_usage": self.age_usage,
            "image_url": self.image_url,
            "status": self.status,
            "admin_notes": self.admin_notes,
            "price": self.price,
            "price_type": self.price_type,
            "location_lat": self.location_lat,
            "location_lng": self.location_lng,
            "location_address": self.location_address,
            "pickup": self.pickup_assignment.to_dict() if self.pickup_assignment else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
