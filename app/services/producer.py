import json
from pika import ConnectionParameters, BlockingConnection
from app.config import settings

connection_params = ConnectionParameters(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT
)

QUEUE_NAME = "email_message"




def send_to_rabbitmq(data: json):

    try:
        with BlockingConnection(connection_params) as conn:
            with conn.channel() as ch:
                ch.queue_declare(queue=QUEUE_NAME)
                ch.basic_publish(
                    exchange="",
                    routing_key=QUEUE_NAME,
                    body=data
                )
    except Exception as e:
        print(f"Error sending data to RabbitMQ: {e}")
