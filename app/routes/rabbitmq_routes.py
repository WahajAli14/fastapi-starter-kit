from fastapi import APIRouter
from rabbitmq_producer import send_message_to_queue
from schema.task_schema import TaskMessage

router = APIRouter()


@router.post("/rabbitmq/send")
def send_message_to_rabbitmq(task_message: TaskMessage):
    """
    Send a message to a RabbitMQ queue.
    """
    try:

        send_message_to_queue(task_message.model_dump())
        return {"message": "Message sent to RabbitMQ queue successfully"}
    except Exception as e:
        return {"error": str(e)}
