from fastapi import APIRouter
from schema.task_schema import TaskMessage
from rabbitmq_producer import send_message_to_queue


router = APIRouter()


@router.post("/rabbitmq/send")
def send_message_to_rabbitmq(task_message: TaskMessage):
    """
    Send a message to a RabbitMQ queue.
    """
    try:
        queue_mapping = {
            "print": "printing_tasks",
            "email": "email_tasks",
            "sms": "sms_tasks"
        }

        queue_name = queue_mapping.get(task_message.task_type, "default_tasks")

        send_message_to_queue( task_message.model_dump())
        return {"message": "Message sent to RabbitMQ queue successfully"}
    except Exception as e:
        return {"error": str(e)}