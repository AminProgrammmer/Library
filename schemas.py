from pydantic import BaseModel,field_validator,EmailStr
from sqlalchemy.orm.session import Session
from fastapi import Depends
from datetime import datetime,timedelta
from db.datebase import Genum
from db.db import get_db
import enum
from typing import List,Dict
class UserBase(BaseModel):
    username : str
    password : str
    email : EmailStr
    date : datetime

    @field_validator("email")
    @classmethod
    def email_validate(cls,value):
        if "gmail" in value and value[-4::] in [".net",".com"]:
            return value
            
        elif "yahoo" in value and value[-4::] in [".net",".com"]:
            return value
        else:
            raise ValueError(f"email {value} dont ready ")



class User_Display(BaseModel):
    id : int
    username : str
    email:str 
    is_admin : int


class LibraryBase(BaseModel):
    name :str
    location :str
    # user_id : int



class BookBase(BaseModel):
    name : str

    author :str

    publish : datetime
    created : datetime
    count:int
    library_id : int    


class BookDisplay(BaseModel):
    name : str
    author :str
    created : datetime
    genere : Genum
    count : int
    library_id : int


class LibraryDisplay(BaseModel):
    id:int
    name :str
    user_id : int
    location :str


class BookDetail(BaseModel):
    name : str
    id : int

class LibraryDetail(BaseModel):
    id:int
    name: str
    user_id : int
    location : str
    books : List[BookDetail]
    total_books : int
    
class Trustbase(BaseModel):
    book_id:int
    delivery_time:datetime = datetime.now()+timedelta(days=7)
    user_id : int