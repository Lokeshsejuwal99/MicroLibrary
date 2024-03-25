
import os
import sys
import pika
import django
import json
from decouple import config
from sys import path
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
path.append(BASE_DIR/'borrow_service/settings.py')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'borrow_service.settings')
django.setup()


#import models here

# RabbitMQ details
RabbitMQ = config("RabbitMQ")
params = pika.URLParameters(RabbitMQ)

# Establish connection to CloudAMQP
connection = pika.BlockingConnection(params)
channel = connection.channel()

def declare_queue(exchange_name, queue_name):
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    result = channel.queue_declare(queue=queue_name, exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name)


def base_consumer(channel, method, properties, body):
    pass
  




# Declare and bind queues 
declare_queue(exchange_name, queue_name)

channel.basic_consume(queue=queue_name, on_message_callback= base_consumer, auto_ack=True)

print("Started Consuming...")
channel.start_consuming()

