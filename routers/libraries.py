from auth.authentication import RoleChecker
from auth.auth2 import get_current_user
from db.db import get_db
from db import db_library
from fastapi import APIRouter , Depends
from sqlalchemy.orm.session import Session
from schemas import LibraryBase,LibraryDisplay,LibraryDetail
from typing import List

router = APIRouter(prefix="/libraries", tags=["libraries"])


@router.post("",response_model=LibraryDisplay)
def create_library(request:LibraryBase,db:Session=Depends(get_db),
                   role = Depends(RoleChecker([2])),
                   current_user = Depends(get_current_user)
                   ):
    
    return db_library.create_library(request,db,current_user)


@router.get("",response_model=List[LibraryDisplay])
def get_libraries(db:Session=Depends(get_db)):
    return db_library.get_libraries(db)


@router.get("/{id}",response_model=List[LibraryDetail])
def get_libraries_by_id(id:int,db:Session=Depends(get_db)):
    return db_library.get_library_by_id(id,db)

@router.delete("/{id}")
def delete_library(id:int,db:Session=Depends(get_db)):
    return db_library.delete_library(id,db)