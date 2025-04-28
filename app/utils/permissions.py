from fastapi import Depends, HTTPException
from functools import wraps
from auth.jwt_bearer import JWTBearer
from typing import Callable, Any

def require_owner_or_admin(get_owner_func: Callable[[int], str | None]):
    """ 
    A decorator for routes that require either the owner or an admin to access.
    """
    def decorator(route_func):
        @wraps(route_func)
        async def wrapper(item_id: int, *args, token=Depends(JWTBearer(["employee", "admin"])), **kwargs):
            owner = get_owner_func(item_id)
            if token["role"] != "admin" and token["username"] != owner:
                raise HTTPException(status_code=403, detail="You are not allowed to perform this action")
            return await route_func(item_id, *args, **kwargs)
        return wrapper
    return decorator
