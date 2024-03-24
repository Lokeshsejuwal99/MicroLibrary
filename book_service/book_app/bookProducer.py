import pika
import json
from decouple import config


def BookProducer(book):
    connection = pika.BlockingConnection(pika.ConnectionParameters(config("RABBITMQ")))
    channel = connection.channel()

    channel.queue_declare(queue="book")

    channel.basic_publish(exchange="", routing_key="book", body=json.dumps(book))

    print(f" [x] book passed  request for = {book}")

    connection.close()
