"""
Seed script – run once to populate default data.
Admin phone: 9999999999  |  OTP: 123456
"""
from app import create_app
from extensions import db
from models.user import User
from models.category import WasteCategory, WasteSubtype
from models.pickup import PickupZone, PickupSlot

CATEGORIES = [
    {"name": "Plastic", "icon": "🧴", "color": "#3B82F6",
     "subtypes": [("Bottles", 15.0, "kg"), ("Bags", 5.0, "kg"), ("Black Plastic", 2.0, "kg"), ("Containers", 10.0, "kg"), ("PVC Pipes", 12.0, "kg")]},
    {"name": "Rubber", "icon": "⚫", "color": "#374151",
     "subtypes": [("Tyres", 20.0, "piece"), ("Rubber Bands", 0.0, "kg"), ("Rubber Sheets", 8.0, "kg"), ("Footwear", 5.0, "kg")]},
    {"name": "Metal", "icon": "🔩", "color": "#6B7280",
     "subtypes": [("Iron/Steel", 25.0, "kg"), ("Aluminium", 120.0, "kg"), ("Copper", 400.0, "kg"), ("Brass", 300.0, "kg"), ("Tin Cans", 15.0, "kg")]},
    {"name": "Paper & Cardboard", "icon": "📦", "color": "#D97706",
     "subtypes": [("Newspapers", 14.0, "kg"), ("Books & Magazines", 10.0, "kg"), ("Cardboard Boxes", 8.0, "kg"), ("Office Paper", 12.0, "kg")]},
    {"name": "Glass", "icon": "🫙", "color": "#06B6D4",
     "subtypes": [("Bottles", 2.0, "kg"), ("Jars", 2.0, "kg"), ("Broken Glass (safe)", 1.0, "kg"), ("Window Glass", 1.0, "kg")]},
    {"name": "Electronics", "icon": "📱", "color": "#8B5CF6",
     "subtypes": [("Mobile Phones", 50.0, "piece"), ("Computers", 200.0, "piece"), ("Cables & Chargers", 20.0, "kg"), ("Batteries", 10.0, "kg"), ("Appliances", 100.0, "piece")]},
    {"name": "Cloth & Textile", "icon": "👕", "color": "#EC4899",
     "subtypes": [("Old Clothes", 5.0, "kg"), ("Torn Fabric", 2.0, "kg"), ("Jute Bags", 5.0, "kg")]},
    {"name": "Wood & Furniture", "icon": "🪑", "color": "#92400E",
     "subtypes": [("Wooden Boards", 2.0, "kg"), ("Broken Furniture", 5.0, "kg"), ("Plywood", 1.0, "kg")]},
]

ZONES = [
    {"name": "Aryabhatta Hostel", "description": "CCSU Boys Hostel"},
    {"name": "Dr. A.P.J. Abdul Kalam Hostel", "description": "CCSU Boys Hostel"},
    {"name": "Dr. B.R. Ambedkar Hostel", "description": "CCSU Boys Hostel"},
    {"name": "Dr. Kailash Prakash Hostel", "description": "CCSU Boys Hostel"},
    {"name": "Dr. R.K. Singh Hostel", "description": "CCSU Boys Hostel"},
    {"name": "Durga Bhabhi Girls Hostel", "description": "CCSU Girls Hostel"},
    {"name": "Rani Lakshmi Bai Girls Hostel", "description": "CCSU Girls Hostel"},
    {"name": "Maharana Pratap Boys Hostel", "description": "CCSU Boys Hostel"},

]

SLOTS = [
    {"date": "2026-04-01", "time_range": "9:00 AM – 12:00 PM", "capacity": 15},
    {"date": "2026-04-01", "time_range": "1:00 PM – 4:00 PM", "capacity": 15},
    {"date": "2026-04-02", "time_range": "9:00 AM – 12:00 PM", "capacity": 15},
    {"date": "2026-04-02", "time_range": "1:00 PM – 4:00 PM", "capacity": 15},
    {"date": "2026-04-03", "time_range": "9:00 AM – 12:00 PM", "capacity": 15},
    {"date": "2026-04-05", "time_range": "9:00 AM – 12:00 PM", "capacity": 20},
    {"date": "2026-04-05", "time_range": "1:00 PM – 4:00 PM", "capacity": 20},
]


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Admin user
        admin = User.query.filter_by(email="admin@trashtreasure.com").first()
        if not admin:
            admin = User(email="admin@trashtreasure.com", name="Super Admin", role="admin", is_verified=True)
            admin.set_password("Admin@123")
            db.session.add(admin)
            print("✅ Admin created: email=admin@trashtreasure.com  Password=Admin@123")
        else:
            print("ℹ️  Admin already exists")

        # Categories & subtypes
        for cat_data in CATEGORIES:
            cat = WasteCategory.query.filter_by(name=cat_data["name"]).first()
            if not cat:
                cat = WasteCategory(
                    name=cat_data["name"],
                    icon=cat_data["icon"],
                    color=cat_data["color"],
                )
                db.session.add(cat)
                db.session.flush()
                for sub in cat_data["subtypes"]:
                    db.session.add(WasteSubtype(category_id=cat.id, name=sub[0], rate_per_unit=sub[1], unit=sub[2]))
                # Always add "Other"
                db.session.add(WasteSubtype(category_id=cat.id, name="Other", rate_per_unit=0.0, unit="kg"))
                print(f"✅ Category: {cat_data['name']}")

        # Pickup zones
        zone_ids = []
        for z in ZONES:
            zone = PickupZone.query.filter_by(name=z["name"]).first()
            if not zone:
                zone = PickupZone(name=z["name"], description=z["description"])
                db.session.add(zone)
                db.session.flush()
                print(f"✅ Zone: {z['name']}")
            zone_ids.append(zone.id)

        # Pickup slots (distributed across zones)
        for i, slot_data in enumerate(SLOTS):
            zone_id = zone_ids[i % len(zone_ids)]
            existing = PickupSlot.query.filter_by(
                date=slot_data["date"], time_range=slot_data["time_range"], zone_id=zone_id
            ).first()
            if not existing:
                slot = PickupSlot(
                    zone_id=zone_id,
                    date=slot_data["date"],
                    time_range=slot_data["time_range"],
                    capacity=slot_data["capacity"],
                )
                db.session.add(slot)

        db.session.commit()
        print("\n🌱 Seed complete!")
        print("   Admin login → email: admin@trashtreasure.com  |  Password: Admin@123")


if __name__ == "__main__":
    seed()


