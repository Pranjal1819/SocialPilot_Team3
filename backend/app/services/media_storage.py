# app/services/media_storage.py
"""
Handles saving uploaded media files to local disk.

Validates the uploaded file against the media_type it's declared as
(image / gif / video / audio / document — same values PostMedia.media_type
and ScheduledPost.content_type expect), enforces a max file size, and
returns a dict shaped like PostMediaItem so the response can be dropped
straight into the `media` list on POST /api/posts/ or PUT /api/posts/{id}.

Swap-out point for later: replace the local-disk write in save_upload()
with an S3/Cloudinary client call and this stays a drop-in replacement
for the rest of the app.
"""

import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings

# --------------------------------------------------
# Allowed extensions per media_type
# --------------------------------------------------

ALLOWED_MEDIA_EXTENSIONS = {
    "image": {".jpg", ".jpeg", ".png", ".webp"},
    "gif": {".gif"},
    "video": {".mp4", ".mov", ".webm"},
    "audio": {".mp3", ".wav", ".m4a", ".aac"},
    "document": {".pdf", ".doc", ".docx"},
}

MAX_UPLOAD_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024


class MediaUploadError(Exception):
    """Raised on any validation failure; the API layer maps this to a 400."""

    pass


def _validate(media_type: str, filename: str, size: int) -> str:

    if media_type not in ALLOWED_MEDIA_EXTENSIONS:

        raise MediaUploadError(
            f"Unsupported media_type '{media_type}'. Must be one of: "
            f"{', '.join(sorted(ALLOWED_MEDIA_EXTENSIONS))}"
        )

    if not filename:

        raise MediaUploadError("Uploaded file has no filename")

    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED_MEDIA_EXTENSIONS[media_type]:

        raise MediaUploadError(
            f"'{ext or 'no extension'}' is not valid for media_type '{media_type}'. "
            f"Allowed: {', '.join(sorted(ALLOWED_MEDIA_EXTENSIONS[media_type]))}"
        )

    if size == 0:

        raise MediaUploadError("Uploaded file is empty")

    if size > MAX_UPLOAD_BYTES:

        raise MediaUploadError(
            f"File is {size / (1024 * 1024):.1f}MB, exceeds the "
            f"{settings.MAX_UPLOAD_SIZE_MB}MB limit"
        )

    return ext


async def save_upload(file: UploadFile, media_type: str, user_id: int) -> dict:
    """
    Validates and writes the upload to disk under
    {UPLOAD_DIR}/{user_id}/{random-name}{ext}.

    Returns a dict with media_url, media_type, mime_type, file_size —
    the same shape as PostMediaItem, minus display_order (caller sets that).
    """

    contents = await file.read()

    ext = _validate(media_type, file.filename, len(contents))

    unique_name = f"{uuid.uuid4().hex}{ext}"

    user_dir = Path(settings.UPLOAD_DIR) / str(user_id)

    user_dir.mkdir(parents=True, exist_ok=True)

    dest_path = user_dir / unique_name

    with open(dest_path, "wb") as f:

        f.write(contents)

    relative_url = f"/uploads/{user_id}/{unique_name}"

    return {
        "media_url": f"{settings.BASE_URL}{relative_url}",
        "file_path": str(dest_path),
        "media_type": media_type,
        "mime_type": file.content_type,
        "file_size": len(contents),
    }
