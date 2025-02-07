from auth.authentication import RoleChecker
from db.db import get_db
from db import trust
from fastapi import APIRouter,Depends
from schemas import Trustbase
from sqlalchemy.orm.session import Session

router = APIRouter(prefix="/trusts",tags=["trust"])

@router.post("")
def add_trust(detail:Trustbase,db:Session=Depends(get_db),role = Depends(RoleChecker([1,2]))):
    return trust.add_trust(detail,db)

@router.delete("/{id}")
def delete_trust(id:int,db:Session=Depends(get_db),role = Depends(RoleChecker([1,2]))):
    return trust.remove_trust(id,db)

@router.get("")
def get_trusts(db:Session=Depends(get_db),role = Depends(RoleChecker([1,2]))):
    return trust.get_trusts(db)


@router.get("/{book_id}")
def get_trust_by_book_id(book_id:int,db:Session=Depends(get_db),role = Depends(RoleChecker([1,2]))):
    return trust.get_by_bookid(book_id,db)
