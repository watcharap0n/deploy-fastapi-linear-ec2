from app.db import db, PyObjectId
from bson import ObjectId
from typing import Optional, Union
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    firstname: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class Register(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    username: str
    email: Union[str, None] = None
    hashed_password: str
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "watcharapon",
                "email": "wera.watcharapon@gmail.com",
                "hashed_password": "kane!@#$",
                "full_name": "watcharapon weeraborirak",
                "disabled": False
            }
        }
