import pika
import json
import logging
import functools
import sys
from utils.messages import send_whatsapp_message, send_email


logging.basicConfig(
    filename='message.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def callback(ch, method, properties, body, args):
    logger = logging.getLogger(__name__)

    message = json.loads(body)
    if message['subject'] in args['subjects']:
        send_email(**message) if args['media'] == 'e-mail' else send_whatsapp_message(**message)
        logger.info(message)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consumer(name, queue, subjects):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue)
    consumer_callback = functools.partial(callback, args={'media': name, 'subjects': subjects})
    channel.basic_consume(queue=queue, on_message_callback=consumer_callback)
    print(f'{name.title()} Consumer waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    name_consumer = sys.argv[1] if sys.argv[1] in ['e-mail', 'whatsapp'] else 'e-mail'
    queue_consumer = sys.argv[2] if sys.argv[2] in ['email_queue', 'whatsapp_queue'] else 'email_queue'
    subjects_consumer = sys.argv[3].split(';')
    consumer(name_consumer, queue_consumer, subjects_consumer)
