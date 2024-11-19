import json
import smtplib
from email.message import EmailMessage
from pika import ConnectionParameters, BlockingConnection
from pydantic import EmailStr
from app.config import settings

smt_host = "smtp.gmail.com"


def get_email_template(code: int, mail: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Подтверждение"
    email["From"] = settings.MAIL_USERNAME
    email["To"] = mail


    email.set_content(f"Подтвердите аккаунт. Ваш код: {code}", subtype="plain")
    email.add_alternative(
        f"<h1>Подтвердите аккаунт</h1><p>{code}-код для завершения аутентификации. На подтверждение аккаунта дается 10 минут.</p>",
        subtype="html"
    )
    return email


connection_params = ConnectionParameters(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT
)

QUEUE_NAME = "email_message"


def callback(ch, method, properties, body):
    try:

        message_data = json.loads(body)
        code = message_data.get("code")
        mail = message_data.get("email")

        if not code or not mail:
            raise ValueError("Missing code or email in message")


        email = get_email_template(code=code, mail=mail)


        with smtplib.SMTP_SSL(smt_host, settings.MAIL_PORT) as server:
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.send_message(email)

    except Exception as e:
      pass

    ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.stop_consuming()


def send_email_to_user():
  with BlockingConnection(connection_params) as conn:
    with conn.channel() as ch:
      ch.queue_declare(queue=QUEUE_NAME)

      ch.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
        )

      ch.start_consuming()
