from db.datebase import User
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from pw_hash import Hash
from datetime import datetime

def create_user(data,db):
    item = User(
    username = data.username,
    password = Hash.bcrypt(data.password),
    email = data.email, 
    date = datetime.now(),
    )
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
        return data
    except IntegrityError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"error : {IntegrityError} please  enter dont duplicate user ")



def get_users(db):
    return db.query(User).all()

def detail_user(id,db):
    return db.query(User).where(User.id ==id).first()



def delete_user(id,db):
    item = db.query(User).where(User.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not in database")
    db.delete(item)
    db.commit()
    return "ok"

def update_user(id,request,db):
    item =db.query(User).where(User.id == id).update({
    "username" : request.username,
    "password" : Hash.bcrypt(request.password),
    "email" : request.email, 
    "date" : datetime.now()
    })
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not in database")
    db.commit()
    return "با موفقیت ویرایش یافت"


def read_user_username(username,db):
    return db.query(User).where(User.username == username).first()


def update_admin(count,id,db):
    query = db.query(User).where(User.id == id).update(
        {"is_admin" : count}
    )
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not in database")
    elif count > 2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you can not set is admin to {count} level ") 
    db.commit()
    return f"User updated to {query} level admin"

