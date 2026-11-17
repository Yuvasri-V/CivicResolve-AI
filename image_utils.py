
from pathlib import Path
from uuid import uuid4

from PIL import Image, UnidentifiedImageError

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_FORMATS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp",
}


def save_uploaded_image(file_bytes: bytes) -> str:
    if not file_bytes:
        raise ValueError("The uploaded image is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("Image size must not exceed 5 MB.")

    try:
        from io import BytesIO

        with Image.open(BytesIO(file_bytes)) as image:
            image_format = image.format

            if image_format not in ALLOWED_FORMATS:
                raise ValueError(
                    "Only JPEG, PNG, and WEBP images are allowed."
                )

            image.verify()

        extension = ALLOWED_FORMATS[image_format]
        filename = f"{uuid4().hex}{extension}"
        destination = UPLOAD_DIR / filename

        destination.write_bytes(file_bytes)

        return f"uploads/{filename}"

    except UnidentifiedImageError:
        raise ValueError("The uploaded file is not a valid image.")
