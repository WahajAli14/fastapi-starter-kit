from fastapi import APIRouter, HTTPException, Depends
from schema.item_schema import Item
from models.user_model import check_if_user_saved, remove_saved_item, save_item_for_user
#from models.item_model import create_item, get_item, get_all_items, delete_item, get_item_owner, search_items, update_item, like_item,change_item_status
from models.item_model import (
    create_item, get_item, get_all_items, delete_item, get_item_owner,
    search_items, update_item, like_item, change_item_status
)
from auth.jwt_bearer import JWTBearer
from utils.permissions import require_owner_or_admin

router = APIRouter()

@router.post("/items/create", response_model=Item)
def add_item(item: Item, owner: dict = Depends(JWTBearer(["employee"]))):
    item_id = create_item(item.model_dump(), owner=owner["username"])
    return {"message": "Item Created", "id": item_id, **item.model_dump()}


@router.get("/items/")
def list_items(_: dict = Depends(JWTBearer(["employee", "user", "admin"]))):
    return get_all_items()


@router.get("/items/search")
def search_items_route(
    q: str = "", category: str = "", limit: int = 10, skip: int = 0,
    _: dict = Depends(JWTBearer(["employee", "user", "admin"]))
):
    query = {}
    if q:
        query["name"] = {"$regex": q, "$options": "i"}
    if category:
        query["category"] = category
    return search_items(query, limit=limit, skip=skip)


@router.get("/items/{item_id}")
def get_item_by_id(item_id: int, _: dict = Depends(JWTBearer(["employee", "admin"]))):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}")
@require_owner_or_admin(get_owner_func=get_item_owner)
async def update_ad(item_id: int, updated_data: dict):
    if update_item(item_id, updated_data):
        return {"message": "Item updated"}
    raise HTTPException(status_code=404, detail="Ad not found")


@router.delete("/items/{item_id}")
#@require_owner_or_admin(get_owner_func=get_item_owner)
async def delete_ad(item_id: int):
    if delete_item(item_id):
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/items/{item_id}/like")
def like_item_route(item_id: int, user: dict = Depends(JWTBearer(["employee", "user", "admin"]))):
    if like_item(item_id):
        return {"message": "Item liked"}
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/items/{item_id}/save")
def save_item_route(item_id: int, user: dict = Depends(JWTBearer(["user", "admin"]))):
    if save_item_for_user(user["username"], item_id):
        return {"message": "Item saved"}
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/items/{item_id}/save")
def remove_saved_item_route(item_id: int, user: dict = Depends(JWTBearer(["user", "admin"]))):
    saved_by_user = check_if_user_saved(user["username"], item_id)
    if not saved_by_user:
        raise HTTPException(status_code=403, detail="You cannot unsave an ad you haven't saved")

    if remove_saved_item(user["username"], item_id):
        return {"message": "Item removed from saved"}
    
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/items/{item_id}/status")
def set_status(item_id: int, status: str, user: dict = Depends(JWTBearer(["admin"]))):
    valid_statuses = ["approved", "pending_review", "sold", "flagged"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {', '.join(valid_statuses)}")
    change_item_status(item_id, status)
    return {"message": f"Ad status set to {status}"}


