from datetime import timezone

from datasbase import db

collection = db["items"]


def create_item(item, owner: str):
    item["id"] = get_next_id()
    item["created_at"] = timezone.utc
    item["owner"] = owner
    item["views"] = 0
    item["likes"] = 0
    item["status"] = "pending_reviews"
    result = collection.insert_one(item)
    return str(result.inserted_id), item["id"]


def get_item_owner(item_id: int) -> str | None:
    item = collection.find_one({"id": item_id}, {"owner": 1, "_id": 0})
    return item["owner"] if item else None


def get_item(item_id: int):
    item = collection.find_one({"id": item_id}, {"_id": 0})
    if item:
        return item
    else:
        return None


def get_all_items():
    items = list(collection.find({}, {"_id": 0}))
    return items


def search_items(q: dict = {}, limit: int = 10, skip: int = 0):
    return list(collection.find(q, {"_id": 0}).skip(skip).limit(limit))


def get_next_id():
    counter = db["counters"]
    result = counter.find_one_and_update(
        {"_id": "itemid"},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True,
    )
    return result["sequence_value"]


def delete_item(item_id: int):
    result = collection.delete_one({"id": item_id})
    return result.deleted_count > 0


def like_item(ad_id: int):
    result = collection.update_one({"id": ad_id}, {"$inc": {"likes": 1}})
    return result.modified_count > 0


def update_item(item_id: int, updated_data: dict):
    protected_fields = ["id", "owner", "created_at", "views", "likes"]
    for field in protected_fields:
        updated_data.pop(field, None)

    result = collection.update_one({"id": item_id}, {"$set": updated_data})
    return result.modified_count > 0


def change_item_status(ad_id: int, status: str):
    inactive_statuses = ["flagged", "sold"]

    update_fields = {
        "status": status,
        "is_active": False if status in inactive_statuses else True,
    }

    result = collection.update_one({"id": ad_id}, {"$set": update_fields})
    return result.modified_count > 0
