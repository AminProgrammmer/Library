from db.datebase import Library,Book
from fastapi import HTTPException,status
from sqlalchemy import func
def create_library(request,db,current):
    data = Library(
    name =request.name,
    location =request.location,
    user_id = current.id
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def get_libraries(db):
    return db.query(Library).all()

def get_library_by_id(id,db):
    for library in db.query(Library).all():
        library.total_books = db.query(func.count(Book.id).filter(Book.library_id ==library.id)).scalar()
    db.commit()
    return db.query(Library).where(Library.id==id).all()



def delete_library(id,db):
    item = db.query(Library).where(Library.id == id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Library not in database")
    db.delete(item)
    db.commit()
    return "ok"

    