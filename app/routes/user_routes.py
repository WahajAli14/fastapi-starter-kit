from fastapi import APIRouter, Depends, HTTPException
from models.user_model import delete_user_by_id, get_all_user_ids
from auth.jwt_bearer import JWTBearer

router = APIRouter()

@router.get("/users/ids")
def fetch_user_ids():  
    return {"user_ids": get_all_user_ids()}

@router.delete("/users/{user_id}")
def delete_user(user_id: str, _: dict = Depends(JWTBearer(["admin"]))): 
    
    if delete_user_by_id(user_id):
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")