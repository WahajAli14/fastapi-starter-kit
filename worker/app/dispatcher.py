import json
from app.tasks.print_tasks import process_printing_task
from app.tasks.email_task import handle_email_task
from app.tasks.generate_pdf_file import generate_pdf_file

def dispatch_task(body):
    data = json.loads(body)

    task_type = data.get("task_type")
    payload = data.get("payload")

    if task_type == "print":
        process_printing_task(payload)
    elif task_type == "email":
        handle_email_task(payload)
    elif task_type == "generate_pdf":
        generate_pdf_file(payload)
    else:
        raise ValueError(f"Unknown task_type: {task_type}")
