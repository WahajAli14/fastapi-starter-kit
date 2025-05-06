import time


def handle_email_task(payload):
    print(f" [📧] Sending Email to: {payload['to']}")
    print(f"Subject: {payload['subject']}")
    print(f"Body: {payload['body']}")
    time.sleep(2)
    print(" [📧] Email Sent Successfully")
