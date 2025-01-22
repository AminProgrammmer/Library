from fastapi import APIRouter,FastAPI,Depends
from contextlib import asynccontextmanager
from db.datebase import Trust
from db.db import session_local,get_db
from db.trust import remove_trust
from datetime import datetime
import time
import asyncio

async def background_task(session):
    while datetime.now().minute != time:
        item = session.query(Trust).all()
        for i in item :
            if i.delivery_time.day < datetime.now().day:
                await remove_trust(id=i.id,db=session)
                
            else:
                pass
        await asyncio.sleep(84600)
    

@asynccontextmanager
async def lifespan(_:FastAPI):
    session = session_local()
    task = asyncio.create_task(background_task(session))
    yield
    task.cancel()
    pass

cronjob = APIRouter(lifespan=lifespan)