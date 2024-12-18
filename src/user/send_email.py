from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

from src.config import MAIL_FROM, MAIL_FROM_NAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USERNAME

class Envs():
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_FROM = MAIL_FROM
    MAIL_PORT = MAIL_PORT
    MAIL_SERVER = MAIL_SERVER
    MAIL_FROM_NAME = MAIL_FROM_NAME

config = ConnectionConfig(
    MAIL_USERNAME = Envs.MAIL_USERNAME,
    MAIL_PASSWORD = Envs.MAIL_PASSWORD,
    MAIL_FROM = Envs.MAIL_FROM,
    MAIL_PORT = Envs.MAIL_PORT,
    MAIL_SERVER = Envs.MAIL_SERVER,
    MAIL_FROM_NAME = Envs.MAIL_FROM_NAME,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    TEMPLATE_FOLDER = "src/user/templates"
)

async def send_registration_email(subject : str, email_to : EmailStr, body : dict) :
    message = MessageSchema(
        subject = subject,
        recipients = [email_to],
        template_body = body,
        subtype = MessageType.html
    )

    fm = FastMail(config)

    await fm.send_message(message = message, template_name = "email.html")

async def password_reset(subject : str, email_to : EmailStr, body : dict) :
    message = MessageSchema(
        subject = subject,
        recipients = [email_to],
        template_body = body,
        subtype = MessageType.html
    )
    
    fm = FastMail(config)

    await fm.send_message(message = message, template_name = "password_reset.html")

async def password_changed(subject : str, email_to : EmailStr, body : dict) :
    message = MessageSchema(
        subject = subject,
        recipients = [email_to],
        template_body = body,
        subtype = MessageType.html
    )
    
    fm = FastMail(config)

    await fm.send_message(message = message, template_name = "password_changed.html")
