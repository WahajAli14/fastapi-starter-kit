import json
import os

import pika
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq-2")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)


def send_message_to_queue(message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()
    queue_name = "printing_tasks"  # Default queue name
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )
    connection.close()
