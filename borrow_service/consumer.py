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

from borrow_app.models import Borrow, Books

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


def book_consumer(channel, method, properties, body):
    message = json.loads(body)
    # Process the message as needed
    print("Received message receive BOOK :", message)
    save = Books.objects.create(
        title=message["title"],
        author=message["author"],
        summary=message["summary"],
        publication_date=message["publication_date"],
        isbn=message["isbn"],
        pages=message["pages"],
        cover=message["cover"],
        quantity=message["quantity"],
    )

    if save:
        print("Book saved successfully")


# Declare and bind queues
declare_queue("borrow_exchange", "borrow_queue")
declare_queue("book_exchange", "book_queue")

channel.basic_consume(
    queue="borrow_queue", on_message_callback=borrow_consumer, auto_ack=True
)
channel.basic_consume(
    queue="book_queue", on_message_callback=book_consumer, auto_ack=True
)

print(" Consuming...")
channel.start_consuming()
