from fastapi import APIRouter, HTTPException
from models.user_model import create_user, find_user_by_username, verify_password
from schema.user_schema import UserRegisterSchema, UserLoginSchema
from auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

FIRST_ADMIN_EMAIL = os.getenv("FIRST_ADMIN_EMAIL")
EMPLOYEE_INVITE_CODE = os.getenv("EMPLOYEE_INVITE_CODE")

auth_router = APIRouter()

@auth_router.post("/register")
def register_user(user: UserRegisterSchema):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = find_user_by_username(user.username)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user_data =user.model_dump(exclude={"confirm_password", "invite_code"})
    
    if user.email == FIRST_ADMIN_EMAIL:
        user_data["role"] = "admin"
    elif user.invite_code == EMPLOYEE_INVITE_CODE:
        user_data["role"] = "employee"
    else:
        user_data["role"] = "user"

    user_id = create_user(user_data)
    return {"message": "User created successfully", "user_id": user_id,  "role": user_data["role"]}

@auth_router.post("/login")
def login_user(user: UserLoginSchema):
    db_user = find_user_by_username(user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    payload={"username": db_user["username"], "role": db_user["role"]}    
    access_token = create_access_token(payload, expires_delta=timedelta(minutes=30))
    refresh_token = create_refresh_token(payload, expires_delta=timedelta(days=7))
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token
    }


@auth_router.post("/refresh-token")
def refresh_token(token: str):
    try:
        payload = decode_token(token)
        if payload is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        new_access_token = create_access_token(payload, expires_delta=timedelta(minutes=30))

        return {
            "access_token": new_access_token
        }
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid token")