import pywhatkit as pwk
import smtplib, ssl
import pathlib
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

        pwk.sendwhatmsg_instantly(recipient, whatsapp_template.render(**kwargs))
        print("Message Sent!")
    except Exception as e:
        print(f"Error in sending the message: {e}")
