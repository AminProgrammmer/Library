from db.datebase import Book
from datetime import datetime
from fastapi import status
from fastapi.exceptions import HTTPException
def add(genere,request,db):
    query = Book(
    name = request.name,
    author =request.author,
    created = request.created,
    publish = datetime.now(),
    library_id = request.library_id,
    genere = genere,
    )
    
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def delete(id,db):
    item = db.query(Book).where(Book.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="book not found")

    db.delete(item)
    db.commit()
    return f"deleted [ {item.name} ] success"


def get_all(db):
    return db.query(Book).all()



def update_book(id,genere,request,db):
    item = db.query(Book).where(Book.id == id).update({
    "name" : request.name,
    "author" :request.author,
    "created" : request.created,
    "library_id" : request.library_id,
    "genere" : genere,
    })
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = "not found id book")
    db.commit()
    return "success"