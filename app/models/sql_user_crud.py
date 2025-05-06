from sqlalchemy.orm import Session
from models.user_model_pg import User
from schema.sql_user_schema import SQLUserRead, SQLUserCreate


def create_ps_user(user: SQLUserCreate, db: Session):
    
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(User).all()

