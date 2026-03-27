import os
import uuid


def save_local_image(file, upload_folder):
    """Save an uploaded image file locally and return its URL path."""
    os.makedirs(upload_folder, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return f"/uploads/{filename}"


def upload_image(file, upload_folder, use_cloudinary=False, cloudinary_config=None):
    """Upload image to Cloudinary if configured, otherwise save locally."""
    if use_cloudinary and cloudinary_config:
        try:
            import cloudinary
            import cloudinary.uploader
            cloudinary.config(
                cloud_name=cloudinary_config.get("cloud_name"),
                api_key=cloudinary_config.get("api_key"),
                api_secret=cloudinary_config.get("api_secret"),
            )
            result = cloudinary.uploader.upload(
                file,
                folder="trashtreasure",
                transformation=[{"width": 800, "crop": "limit"}],
                timeout=60,
            )
            return result["secure_url"]
        except Exception as e:
            print(f"Cloudinary upload failed: {e}, falling back to local storage")

    return save_local_image(file, upload_folder)
