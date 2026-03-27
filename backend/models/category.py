from datetime import datetime
from extensions import db


class WasteCategory(db.Model):
    __tablename__ = "waste_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10), default="♻️")
    color = db.Column(db.String(20), default="#4CAF71")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    subtypes = db.relationship("WasteSubtype", backref="category", lazy=True)

    def to_dict(self, include_subtypes=True):
        data = {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "color": self.color,
            "is_active": self.is_active,
        }
        if include_subtypes:
            data["subtypes"] = [s.to_dict() for s in self.subtypes if s.is_active]
        return data


class WasteSubtype(db.Model):
    __tablename__ = "waste_subtypes"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("waste_categories.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    rate_per_unit = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(20), default="kg")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "is_active": self.is_active,
            "rate_per_unit": self.rate_per_unit,
            "unit": self.unit,
        }
