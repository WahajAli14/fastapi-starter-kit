from pydantic import BaseModel
from typing import Dict, Any

class TaskMessage(BaseModel):
    task_type: str
    payload: Dict[str, Any]
