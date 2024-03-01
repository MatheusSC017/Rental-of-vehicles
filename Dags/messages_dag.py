from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pika
import json
import requests
from config import *


def send_message(message, queue_name):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
        connection.close()
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {str(e)}")


def send_email_message():
    headers = {
        "Authorization": ACCESS_TOKEN
    }
    response = requests.get(API_URL, headers=headers)
    messages = json.loads(response.content)
    if len(messages):
        for message in messages:
            send_message(message, 'email_queue')


def send_whatsapp_message():
    headers = {
        "Authorization": ACCESS_TOKEN
    }
    response = requests.get(API_URL, headers=headers)
    messages = json.loads(response.content)
    if len(messages):
        for message in messages:
            send_message(message, 'whatsapp_queue')


with DAG(dag_id="messages",
         start_date=datetime.today(),
         schedule_interval="@daily",
         catchup=False) as dag:

    email_task = PythonOperator(
        task_id="send_email_message",
        python_callable=send_email_message
    )

    whatsapp_task = PythonOperator(
        task_id="send_whatsapp_message",
        python_callable=send_whatsapp_message
    )
