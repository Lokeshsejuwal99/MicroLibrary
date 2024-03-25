import os
import sys
import pika
import django
import json
from decouple import config
from sys import path
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
import sys

sys.path.append(str(BASE_DIR / "borrow_service"))

path.append(BASE_DIR / "borrow_service/settings.py")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "borrow_service.settings")
django.setup()

from borrow_app.models import Borrow

# import models here

# RabbitMQ details
RabbitMQ = config("RABBITMQ")
params = pika.URLParameters(RabbitMQ)

# Establish connection to CloudAMQP
connection = pika.BlockingConnection(params)
channel = connection.channel()


def declare_queue(exchange_name, queue_name):
    channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")
    result = channel.queue_declare(queue=queue_name)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name)


def borrow_consumer(channel, method, properties, body):
    message = json.loads(body)
    # Process the message as needed
    print("Received message:", message)
    save = Borrow.objects.create(
        user_id=message["user_id"],
        book_id=message["book_id"],
        borrow_date=message["borrow_date"],
        due_date=message["due_date"],
        returned=message["returned"],
        return_date=message["return_date"],
    )

    if save:
        print("Borrow saved successfully")
    # channel.basic_ack(delivery_tag=method.delivery_tag)


# Declare and bind queues
declare_queue("borrow_exchange", "borrow_queue")

channel.basic_consume(
    queue="borrow_queue", on_message_callback=borrow_consumer, auto_ack=True
)

print("Started Consuming...")
channel.start_consuming()
