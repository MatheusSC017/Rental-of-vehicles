import smtplib, ssl
import pathlib
import requests
import os
from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
template_env = Environment(loader=FileSystemLoader(searchpath="Consumers/templates"))
try:
    load_dotenv(BASE_DIR.parent / ".env.consumers")
except:
    load_dotenv(BASE_DIR.parent / ".env")

if os.getenv("WHATSAPP_TEST_URL"):
    WHATSAPP_URL = "https://waba-sandbox.360dialog.io/v1/messages"
else:
    WHATSAPP_URL = "https://waba.360dialog.io/v1/messages"


def send_email(recipient, subject, **kwargs):
    try:
        context = ssl.create_default_context()
        email_template = template_env.get_template(f"email/{subject.replace(' ', '_')}.html")
        email_content = email_template.render(subject=subject.title(), **kwargs)

        # Create the email message
        msg = MIMEText(email_content, 'html')
        msg['Subject'] = subject.title()
        msg['From'] = os.getenv("EMAIL")
        msg['To'] = recipient

        with smtplib.SMTP_SSL("smtp.gmail.com", os.getenv("PORT"), context=context) as server:
            server.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
            server.sendmail(os.getenv("EMAIL"), recipient, msg.as_string())
        print("Message Sent!")
    except Exception as e:
        print(f"Error in sending the message: {e}")


def send_whatsapp_message(recipient, subject, **kwargs):
    try:
        whatsapp_template = template_env.get_template(f"whatsapp/{subject.replace(' ', '_')}.html")

        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": ''.join([c for c in recipient if c.isdigit()]),
            "type": "text",
            "text": {
                "body": whatsapp_template.render(**kwargs)
            }
        }

        headers = {
            "D360-API-KEY": os.getenv("WHATSAPP_KEY")
        }

        response = requests.post(WHATSAPP_URL, json=data, headers=headers)

        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            raise Exception(response)
    except Exception as e:
        print(f"Error in sending the message: {e}")
