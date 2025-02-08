from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager

from db.datebase import Trust, User
from db.db import session_local
from datetime import datetime
from datetime import datetime,timedelta

import send_email
import asyncio
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def background_task(session):
    while True:
        
        try:
            first_user = session.query(User).where(User.id == 1).update({
            "is_admin": 2,
            "expire_date" : datetime.now() + timedelta(weeks=99999)
                })
            
            users = session.query(User).all()
            for u in users:
                if u.expire_date < datetime.now():
                    print("yeah , your status will be set false")
                    session.query(User).where(User.id == u.id).update({
                        "status": False,
                        "delay_penalty" : u.delay_penalty + 20000
                    })
                    
                    email=send_email.EmailSchema(
                        email=[u.email],
                        subject=f"پایان اعتبار حساب کتابخانه شما!",
                        body=f"""  
                        شما باید حساب خود را به پاس استفاده تمدید نمایید ! میزان جریمه فعلی را مشاهده میکنید !  وئ مبلغ 20000 تومان هم
                        به جریمه شما به عنوان حق التمدید اضافه میشود !
                        پس از پرداخت وضعیت اکانت شما فعال خواهد 
                        شد
                        
                         پرداخت کنید : {u.delay_penalty}"""
                    )
                    send_email.send_email(email=email)
                    
                else :
                    print("email have time")
                    
                    
            items = session.query(Trust).all()
            for t in items:
                if t.delivery_time < datetime.now():
                    
                    session.query(User).where(t.delivery_time < datetime.now() and User.id == t.user.id).update({
                        "delay_penalty" : t.user.delay_penalty + 200
                    })
                
                    
                    email=send_email.EmailSchema(
                        email=[t.user.email],
                        subject=f"اتمام امانت کتاب {t.book.name}",
                        body=f" درود 7 روز زمان امانت کتاب شما به اتمام رسید !! شما از لیست کتابداران امانت خط میخورید و به اضای هر روز تاخیر 200تومان جریمه میشوید جریمه فعلی شما {t.user.delay_penalty}"
                    )
                    send_email.send_email(email=email)
                else:
                    logger.info("Delivery time not reached yet")
        except Exception as e:
            logger.error(f"Error in background task: {e}")
        session.commit()
        await asyncio.sleep(delay=86400)
        
@asynccontextmanager
async def lifespan(_: FastAPI):
    session = session_local()
    task = asyncio.create_task(background_task(session))
    try:
        yield
    finally:
        task.cancel()
        session.close()
cronjob = APIRouter(lifespan=lifespan)
