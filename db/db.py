from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

engine = create_engine("sqlite:///library.db")
session_local = sessionmaker(bind=engine)
base = declarative_base()

def get_db():
    session = session_local()
    try:
        yield session
    finally:
        session.close()