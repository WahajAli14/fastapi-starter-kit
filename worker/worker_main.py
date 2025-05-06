from app.consumer import WorkerConsumer


def main():
    consumer = WorkerConsumer(queue_name="printing_tasks")
    consumer.start()


if __name__ == "__main__":
    main()
