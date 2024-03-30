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

sys.path.append(str(BASE_DIR / "book_service"))

path.append(BASE_DIR / "book_service/settings.py")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_service.settings")
django.setup()

from book_app.models import Books
from django.shortcuts import get_object_or_404


RabbitMQ = config("RABBITMQ")
params = pika.URLParameters(RabbitMQ)

connection = pika.BlockingConnection(params)
channel = connection.channel()


def declare_queue(exchange_name, queue_name):
    channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")
    channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=exchange_name, queue=queue_name)


def borrow_consumer(channel, method, properties, body):
    message = json.loads(body)
    print("Received message:", message)
    book_id = message.get("book_id")  # Get the book_id from the message
    if book_id is not None:
        book = get_object_or_404(Books, id=book_id)  # Retrieve the Book object
        print("Received message:", message)
        print("Book:", book)
    else:
        print("Missing book_id in message:", message)


# Declare and bind queues
declare_queue("borrow_book_exchange", "borrow_book_queue")

channel.basic_consume(
    queue="borrow_book_queue", on_message_callback=borrow_consumer, auto_ack=True
)

print("Started Consuming...")
channel.start_consuming()
