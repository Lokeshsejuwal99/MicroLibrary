import pika
import json
from decouple import config


def BookProducer(book):
    print("BookProducer")
    amqp_url = config("RABBITMQ")  # Use your environment variable for the AMQP URL

    connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
    channel = connection.channel()

    channel.queue_declare(queue="borrow_queue")

    channel.basic_publish(
        exchange="borrow_exchange", routing_key="borrow_queue", body=json.dumps(book)
    )

    print(f" [x] Book request published: {book}")

    connection.close()


# Call the function with your book data
