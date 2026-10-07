from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.users import Users

class UserRegister(BaseModel):
    username:str
    email:EmailStr
    password:str = Field(
        min_length=8,
        max_length=55,
    )

class UserLogin(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    username:str
    email:EmailStr
    password:str
    created_at:datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class TokenResponse(BaseModel):
    access_token:str
    token_type:str