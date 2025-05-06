from bson.objectid import ObjectId
from datasbase import async_db, db
from passlib.hash import bcrypt

user_collection = db["users"]
item_collection = db["items"]
async_user_collection = async_db["users"]


def create_user(data):
    data["password"] = bcrypt.hash(data["password"])
    result = user_collection.insert_one(data)
    return str(result.inserted_id)


def find_user_by_username(username):
    user = user_collection.find_one({"username": username})
    if user:
        return user
    else:
        return None


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def save_item_for_user(username, item_id):
    item_exists = item_collection.find_one({"_id": item_id})

    if not item_exists:
        return {"success": False, "message": "Item not found"}

    result = user_collection.update_one(
        {"username": username}, {"$addToSet": {"saved_items": item_id}}
    )

    if result.modified_count > 0:
        return {"success": True, "message": "Item saved successfully"}
    else:
        return {"success": False, "message": "Item already saved or user not found"}


def remove_saved_item(username: str, ad_id: int):
    return user_collection.update_one(
        {"username": username}, {"$pull": {"saved_ads": ad_id}}
    )


def check_if_user_saved(username: str, item_id: int):
    user = user_collection.find_one({"username": username})
    if user:
        return item_id in user.get("saved_ads", [])
    return False


def get_all_user_ids():
    users = user_collection.find({}, {"_id": 1, "username": 1})
    return [{"id": str(user["_id"]), "username": user["username"]} for user in users]


async def get_all_user_ids_async():
    users = async_user_collection.find({}, {"_id": 1, "username": 1})
    cursor = await users.to_list(length=1000)
    return [{"id": str(user["_id"]), "username": user["username"]} for user in cursor]


def delete_user_by_id(user_id: str):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
