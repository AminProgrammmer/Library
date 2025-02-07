from auth.auth2 import oauth2_scheme
from auth.authentication import RoleChecker

from db.db import get_db
from db import db_user

from fastapi import APIRouter,Depends,status
from sqlalchemy.orm.session import Session
from schemas import UserBase,User_Display
from typing import List


router = APIRouter(prefix="/users",tags=["users"])

def write_log(message):
    with open("log.txt","+a") as f:
        f.write(message + " \n")


@router.post("")
def create_user(request:UserBase,db:Session=Depends(get_db)):
    write_log(f"added a user . detail : {request.username} by email : {request.email}")
    return db_user.create_user(request,db)



@router.get("",response_model=List[User_Display])
def get_user(db:Session=Depends(get_db),current_user=Depends(oauth2_scheme),role = Depends(RoleChecker([2]))):
    write_log("got all users")
    return db_user.get_users(db=db)



@router.get("/{id}")
def detail_user(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2_scheme),role = Depends(RoleChecker([2]))):
    write_log(f"got detail user by id {id}")

    return db_user.detail_user(id=id,db=db)



@router.delete("/{id}")
def delete_user(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2_scheme),role = Depends(RoleChecker([2]))):
    write_log(f"request for delete user by id {id}")

    return db_user.delete_user(id=id,db=db)


@router.put("/{id}")
def update_user(id:int,request:UserBase,db:Session=Depends(get_db),current_user=Depends(oauth2_scheme),role = Depends(RoleChecker([2]))):
    write_log(f"updated user by id {id}")

    return db_user.update_user(id=id,request=request,db=db)


@router.put("/upgrade-admin/{id}")
def upgrade_user(count : int,id:int,db:Session=Depends(get_db),role = Depends(RoleChecker([2]))):
    write_log(f"upgrade user by id {id} to {count} level admin")
    return db_user.update_admin(count=count,id=id,db=db)


