import time


def process_printing_task(payload):
    print(f" [🖨] Printing: {payload}")
    time.sleep(1)
    print(" [🖨] Printing Completed")
