from pydantic import BaseModel,field_validator,EmailStr
from sqlalchemy.orm.session import Session
from fastapi import Depends
from datetime import datetime,timedelta
from db.datebase import Genum
from db.db import get_db
import re
from typing import List

class UserBase(BaseModel):
    username : str
    password : str
    email : EmailStr
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search("[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search("[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search("[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search("[@#$%^&+=]", v):
            raise ValueError("Password must contain at least one special character (@#$%^&+=)")
        return v
    
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
    status : bool
    username : str
    email:str 
    is_admin : int
    expire_date : datetime


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