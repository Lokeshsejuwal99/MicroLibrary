import pika
import json
import sys
from sys import path
from decouple import config
import os
import django

print(sys.path)

from pathlib import Path


# project_path = "C:\\Users\\4\\RoleManagement\\role"
project_path = (
    Path(__file__).resolve().parents[2]
)  # This is the path to the project root directory


sys.path.append(project_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "borrow_service.settings")
django.setup()


# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host=config("RABBITMQ")))
channel = connection.channel()

# Declare a queue for the consumer (it will bind to the fanout exchange)
queue_name = "organization"
channel.queue_declare(queue=queue_name)

# Declare the fanout exchange and bind the queue to it
exchange_name = "book_exchange"
channel.exchange_declare(exchange=exchange_name, exchange_type="direct")
channel.queue_bind(exchange=exchange_name, queue=queue_name)


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(data)


# Start consuming messages from the queue
print("Waiting for messages...")
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
