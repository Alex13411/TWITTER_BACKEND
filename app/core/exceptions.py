# app/core/exceptions.py
from fastapi import HTTPException


class TwitterException(HTTPException):
    def __init__(self, status_code: int, error_type: str, error_message: str):
        super().__init__(status_code=status_code, detail=error_message)
        self.error_type = error_type
        self.error_message = error_message