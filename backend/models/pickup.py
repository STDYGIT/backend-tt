from datetime import datetime
from extensions import db


class PickupZone(db.Model):
    __tablename__ = "pickup_zones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    slots = db.relationship("PickupSlot", backref="zone", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
        }


class PickupSlot(db.Model):
    __tablename__ = "pickup_slots"

    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey("pickup_zones.id"), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    time_range = db.Column(db.String(50), nullable=False)  # e.g. "9AM - 12PM"
    capacity = db.Column(db.Integer, default=10)
    booked_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "zone_id": self.zone_id,
            "zone_name": self.zone.name if self.zone else None,
            "date": self.date,
            "time_range": self.time_range,
            "capacity": self.capacity,
            "booked_count": self.booked_count,
            "available": self.capacity - self.booked_count,
            "is_active": self.is_active,
        }


class PickupAssignment(db.Model):
    __tablename__ = "pickup_assignments"

    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("waste_entries.id"), nullable=False, unique=True)
    slot_id = db.Column(db.Integer, db.ForeignKey("pickup_slots.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)

    slot = db.relationship("PickupSlot", backref="assignments")

    def to_dict(self):
        return {
            "id": self.id,
            "entry_id": self.entry_id,
            "slot": self.slot.to_dict() if self.slot else None,
            "assigned_at": self.assigned_at.isoformat(),
        }
