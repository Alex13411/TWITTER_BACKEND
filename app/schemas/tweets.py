from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.users import UserShort

# --- Схемы для POST /api/tweets ---
class TweetCreate(BaseModel):
    tweet_data: str = Field(..., description="Текст твита")
    tweet_media_ids: Optional[List[int]] = Field(default=[], description="ID загруженных картинок")

class TweetCreateResponse(BaseModel):
    result: bool = True
    tweet_id: int

# --- Схемы для POST /api/medias ---
class MediaResponse(BaseModel):
    result: bool = True
    media_id: int

# --- Схемы для ленты твитов GET /api/tweets ---
class TweetLikeInfo(BaseModel):
    user_id: int
    name: str

    class Config:
        from_attributes = True

class TweetOut(BaseModel):
    id: int
    content: str = Field(..., alias="content")  
    attachments: List[str] = Field(default=[], description="Ссылки на изображения")  
    author: UserShort
    likes: List[TweetLikeInfo] = Field(default=[])  

    class Config:
        from_attributes = True
        populate_by_name = True

class TweetListResponse(BaseModel):
    result: bool = True
    tweets: List[TweetOut]  