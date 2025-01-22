from sqlalchemy import DateTime,Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
import enum
from db import db
from datetime import datetime, timedelta
class Genum(enum.Enum):
    DRAMA = "DRAMA"
    COMIDIC = "COMEDIC"
    motivational = "motivational"

class User(db.base):
    __tablename__ = "user"
    id = Column(Integer,index=True,primary_key=True)
    username = Column(String(20),unique=True)
    password = Column(String)
    email = Column(String)
    date = Column(DateTime)
    expire_date = Column(DateTime)
    is_admin = Column(Integer,default=0)
    trust = relationship("Trust",back_populates="user")
    library = relationship("Library",back_populates="user")


class Library(db.base):
    __tablename__ = "library"
    id = Column(Integer,index=True,primary_key=True)
    name = Column(String)
    location = Column(String)
    user_id = Column(Integer,ForeignKey("user.id"))
    user = relationship("User",back_populates="library")
    books =  relationship("Book",back_populates="library")
    total_books = Column(Integer,default=0)

class Book(db.base):
    __tablename__ = "book"
    id = Column(Integer,index=True,primary_key=True)
    name = Column(String)
    author = Column(String)
    created = Column(DateTime)
    publish = Column(DateTime)
    genere = Column(Enum(Genum))
    count = Column(Integer,default=1)
    library_id = Column(Integer,ForeignKey("library.id"))
    library = relationship("Library",back_populates="books")
    trust = relationship("Trust",back_populates="book")

class Trust(db.base):
    __tablename__ = "Trust"
    id = Column(Integer,index=True,primary_key=True)
    book_id = Column(Integer,ForeignKey("book.id"))
    delivery_time = Column(DateTime,default=datetime.now()+timedelta(days=7))
    user_id = Column(Integer,ForeignKey("user.id"))
    user = relationship("User",back_populates="trust")
    book = relationship("Book",back_populates="trust")
