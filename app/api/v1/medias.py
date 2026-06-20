import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.base import Media, User
from app.schemas.tweets import MediaResponse

router = APIRouter()

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/medias", response_model=MediaResponse)
def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Уникальное имя, чтобы файлы не перезаписывали друг друга
    extension = Path(file.filename).suffix if file.filename else ""
    filename = f"{uuid.uuid4()}{extension}"
    disk_path = UPLOAD_DIR / filename

    # Сохраняем файл на диск
    with open(disk_path, "wb") as f:
        f.write(file.file.read())

    # Путь в БД — относительно папки static (для ссылок позже)
    media = Media(
        file_path=f"uploads/{filename}",
        tweet_id=None,
    )
    db.add(media)
    db.commit()
    db.refresh(media)

    return MediaResponse(result=True, media_id=media.id)