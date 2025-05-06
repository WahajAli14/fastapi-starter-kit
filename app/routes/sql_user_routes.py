# app/routes/sql_user_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sql_database import get_sql_db
from schema.sql_user_schema import SQLUserCreate, SQLUserRead
from models.user_model_pg import User
from passlib.hash import bcrypt
from models.sql_user_crud import create_ps_user, get_all_users

router = APIRouter(prefix="/sql-users", tags=["SQL Users"])

@router.post("/", response_model=SQLUserRead)
def create_sql_user(user: SQLUserCreate, db: Session = Depends(get_sql_db)):
    hashed_pw = bcrypt.hash(user.password)
    user.password = hashed_pw
    db_user = create_ps_user(user, db)
    return db_user

@router.get("/", response_model=list[SQLUserRead])
def read_sql_users(db: Session = Depends(get_sql_db)):
    users = get_all_users(db)
    return users