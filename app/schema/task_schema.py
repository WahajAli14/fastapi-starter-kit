from typing import Any, Dict

from pydantic import BaseModel


class TaskMessage(BaseModel):
    task_type: str
    payload: Dict[str, Any]
