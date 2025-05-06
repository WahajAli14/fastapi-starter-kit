import pika


class RabbitMQConnection:
    def __init__(self, host: str = "rabbitmq-2"):
        self.host = host
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()
        return self.channel

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
