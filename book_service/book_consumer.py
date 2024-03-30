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

# from borrow_app.models import Borrow


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


# Declare and bind queues
declare_queue("borrow_book_exchange", "borrow_book_queue")

channel.basic_consume(
    queue="borrow_book_queue", on_message_callback=borrow_consumer, auto_ack=True
)

print("Started Consuming...")
channel.start_consuming()
