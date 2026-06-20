from fastapi import Header, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.base import User
from app.core.exceptions import TwitterException

def get_current_user(
    api_key: str = Header(..., alias="api-key"),
    db: Session = Depends(get_db),
) -> User:
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise TwitterException(
            status_code=401,
            error_type="Unauthenticated",
            error_message="Неверный или отсутствующий API-ключ.",
        )
    return user