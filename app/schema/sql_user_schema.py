from pydantic import BaseModel, EmailStr

class SQLUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class SQLUserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True