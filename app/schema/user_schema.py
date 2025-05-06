from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: EmailStr
    invite_code: str | None = None


class UserLoginSchema(BaseModel):
    username: str
    password: str
