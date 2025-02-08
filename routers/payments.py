from auth.authentication import RoleChecker
from fastapi import APIRouter , Depends,HTTPException,status
from sqlalchemy.orm.session import Session
from schemas import LibraryBase,LibraryDisplay,LibraryDetail
from db.db import get_db
from db.datebase import User
from datetime import timedelta,datetime
from db import db_library

from typing import List
router = APIRouter(prefix="/paymants", tags=["paymants"])

@router.post("")
def paymant_user(id:int,db:Session =Depends(get_db),role=Depends(RoleChecker([2,1]))):
    users = db.query(User).where(User.id == id).update({
        "status" : True,
        "expire_date" : datetime.now() + timedelta(weeks=48),
        "delay_penalty" : 0
    })
    db.commit()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found in list")
    return "success user set the enable"
