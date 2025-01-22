from fastapi import APIRouter , Depends
from sqlalchemy.orm.session import Session
from schemas import BookBase,BookDisplay
from db.db import get_db
from db import db_book
from db.datebase import Genum
from auth.authentication import RoleChecker
from auth.auth2 import get_current_user
from routers.user import write_log
from typing import List

router = APIRouter(prefix="/books", tags=["books"])

@router.post("",response_model=BookDisplay)
def add_book(genere:Genum,request:BookBase,db:Session=Depends(get_db),role = Depends(RoleChecker([1,2]))):
    return db_book.add(genere,request,db)
    

@router.delete("/{id}")
def remove_book(id:int,db:Session=Depends(get_db),role = Depends(RoleChecker([1,2]))):
    return db_book.delete(id,db)
    
@router.get("",response_model=List[BookDisplay])
def get_all_books(db:Session=Depends(get_db)):
    return db_book.get_all(db)


@router.put("/{id}")
def update_book(id:int,genere:Genum,request:BookBase,db:Session=Depends(get_db),role = Depends(RoleChecker([2]))):
    write_log(f"updated book by id {id}")
    return db_book.update_book(id=id,genere = genere,request=request,db=db)