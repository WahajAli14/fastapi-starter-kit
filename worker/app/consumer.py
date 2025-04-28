from app.connection import RabbitMQConnection
from app.dispatcher import dispatch_task

class WorkerConsumer:
    def __init__(self, queue_name: str = "printing_tasks"):
        self.queue_name = queue_name
        self.connection_manager = RabbitMQConnection()

    def start(self):
        channel = self.connection_manager.connect()

        channel.queue_declare(queue=self.queue_name, durable=True)

        def callback(ch, method, properties, body):
            try:
                dispatch_task(body)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f" [!] Error processing message: {e}")

                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.queue_name, on_message_callback=callback)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
