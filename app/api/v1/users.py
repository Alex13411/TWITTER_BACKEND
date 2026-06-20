from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.base import User
from app.schemas.users import UserProfileResponse
from app.core.exceptions import TwitterException
from app.schemas.common import SuccessResponse

router = APIRouter()
@router.get("/users/me", response_model=UserProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.refresh(current_user)
    return UserProfileResponse(
        result=True,
        user=current_user,
    )
@router.get("/users/{user_id}", response_model=UserProfileResponse)
def get_user_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise TwitterException(status_code=404, error_type="UserNotFound", error_message="Пользователь не найден")
    return UserProfileResponse(
        result=True,
        user=user,
    )
@router.post("/users/{user_id}/follow", response_model=SuccessResponse)
def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id == current_user.id:
        raise TwitterException(
            status_code=400,
            error_type="BadRequest",
            error_message="Нельзя подписаться на самого себя.",
        )
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise TwitterException(
            status_code=404,
            error_type="NotFound",
            error_message=f"Пользователь с id={user_id} не найден.",
        )
    if target in current_user.following:
        raise TwitterException(
            status_code=400,
            error_type="BadRequest",
            error_message="Вы уже подписаны на этого пользователя.",
        )
    current_user.following.append(target)
    db.commit()
    return SuccessResponse(result=True)
@router.delete("/users/{user_id}/follow", response_model=SuccessResponse)
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise TwitterException(
            status_code=404,
            error_type="NotFound",
            error_message=f"Пользователь с id={user_id} не найден.",
        )
    if target not in current_user.following:
        raise TwitterException(
            status_code=400,
            error_type="BadRequest",
            error_message="Вы не подписаны на этого пользователя.",
        )
    current_user.following.remove(target)
    db.commit()
    return SuccessResponse(result=True)