from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    email : EmailStr = Field(...)


class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
