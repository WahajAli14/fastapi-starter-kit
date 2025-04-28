from datetime import datetime
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None
    price: float
    category: str | None
    is_active: bool = True
    created_at: datetime | None = None
    owner : str | None = None
    views : int = 0
    likes : int = 0
    status : str = "pending_reviews"

