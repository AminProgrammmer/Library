from fastapi import FastAPI,Request,Depends
from routers import user,libraries,books,trust,cronjob
from auth import authentication
from db.db import base,engine
import send_email

app = FastAPI()

app.include_router(cronjob.cronjob)
app.include_router(send_email.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(libraries.router)
app.include_router(books.router)
app.include_router(trust.router)

base.metadata.create_all(engine)
@app.get("")
def Home():
    return "hello to home page"




