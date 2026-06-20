from typing import List

from pydantic import BaseModel


class UserShort(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    id: int
    name: str
    followers: List[UserShort]
    following: List[UserShort]

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    result: bool = True
    user: UserProfile