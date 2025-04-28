import json
from app.tasks.print_tasks import process_printing_task
from app.tasks.email_task import handle_email_task

def dispatch_task(body):
    data = json.loads(body)

    task_type = data.get("task_type")
    payload = data.get("payload")

    if task_type == "print":
        process_printing_task(payload)
    elif task_type == "email":
        handle_email_task(payload)
    else:
        raise ValueError(f"Unknown task_type: {task_type}")
