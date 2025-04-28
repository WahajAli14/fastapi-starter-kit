from pydantic import BaseModel, EmailStr
from typing import Literal

class UserRegisterSchema(BaseModel):
    username: str 
    password: str
    confirm_password: str
    email: EmailStr
    invite_code: str | None = None

class UserLoginSchema(BaseModel):
    username: str
    password: str