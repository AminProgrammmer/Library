from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel,SecretStr
from typing import List
import smtplib
router = APIRouter(prefix="/Emails")

class EmailSchema(BaseModel):
   email: List[EmailStr]


# حالا پیکربندی را ایجاد کنید
conf = ConnectionConfig(
    MAIL_USERNAME="amin12387amin@gmail.com",
    MAIL_PASSWORD="djwf hlap wono mynb",
    MAIL_FROM="yzdym9931@gmail.com",
    MAIL_PORT=587,  # برای TLS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="amin",
    MAIL_STARTTLS=True,  # فعال کردن TLS
    MAIL_SSL_TLS=False,   # غیرفعال کردن SSL
    USE_CREDENTIALS=True,
)

@router.post("/send_email")
async def send_mail(email: EmailSchema):
	template = """
		<html>
		<body>
		

<p>Hi !!!
		<br>Thanks for using fastapi mail, keep using it..!!!</p>


		</body>
		</html>
		"""

	message = MessageSchema(
		subject="Fastapi-Mail module",
		recipients=email.dict().get("email"), # List of recipients, as many as you can pass 
		body=template,
		subtype="html"
		)

	# fm = FastMail(conf)
	# await fm.send_message(message)
	# print(message)
 
 

	
	server = smtplib.SMTP(conf.MAIL_SERVER,conf.MAIL_PORT)
	server.starttls()
	server.login(conf.MAIL_FROM_NAME,conf.MAIL_PASSWORD.get_secret_value())
	server.sendmail(from_addr=conf.MAIL_FROM_NAME,to_addrs=email,msg=message)
	return JSONResponse(status_code=200, content={"message": "email has been sent"})
