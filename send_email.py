from fastapi import APIRouter, Request, Query, HTTPException
from fastapi_mail import MessageSchema, ConnectionConfig
from fastapi.templating import Jinja2Templates

from pydantic import EmailStr, BaseModel, SecretStr
from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
import smtplib

router = APIRouter(prefix="/Emails")
template = Jinja2Templates(directory="templates/")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailSchema(BaseModel):
    email:List[EmailStr]
    subject: str
    body: str

conf = ConnectionConfig(
    MAIL_USERNAME="a16685091@gmail.com",
    MAIL_PASSWORD=SecretStr("pivu xeyv xidy qcih"),
    MAIL_FROM="a16685091@gmail.com",
    MAIL_PORT=587,  # برای TLS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Fastapi",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

@router.post("/send_email")
def send_email(email: EmailSchema):
    try:
        message = MessageSchema(
            subject=email.subject,
            recipients=email.email,
            body=template.get_template("email.html").render(subject=email.subject, body=email.body),
            subtype="html"
        )

        msg = MIMEMultipart()
        msg['From'] = conf.MAIL_FROM
        msg['To'] = ", ".join(message.recipients)
        msg['Subject'] = message.subject

        msg.attach(MIMEText(message.body, 'html'))

        server = smtplib.SMTP(conf.MAIL_SERVER, conf.MAIL_PORT)
        server.starttls()
        server.login(conf.MAIL_USERNAME, conf.MAIL_PASSWORD.get_secret_value())
        server.send_message(msg)
        server.quit()

        return {"message": "Email has been sent"}

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="There was an error sending the email")
