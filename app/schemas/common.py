from pydantic import BaseModel


class SuccessResponse(BaseModel):
    result: bool = True

class ErrorResponse(BaseModel):
    result: bool = False
    error_type: str
    error_message: str