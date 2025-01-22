from db.datebase import Trust,Book,User
from fastapi import HTTPException
from fastapi import status

def add_trust(detail,db):
    item = Trust(
        book_id = detail.book_id,
        delivery_time = detail.delivery_time,
        user_id = detail.user_id
    )
    count_book = db.query(Book).where(Book.id==detail.book_id).first()
    if not db.query(Book).where(detail.book_id==Book.id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not defined")
    elif not db.query(User).where(User.id==detail.user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found user")
    elif count_book.count >= 1:
        count_book.count -= 1
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    else :
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="count book lower than 1")

def remove_trust(id,db):
    item = db.query(Trust).where(Trust.id == id).first()
    if item:
        count_book = db.query(Book).where(Book.id==item.book_id).first()
        count_book.count += 1
        print(count_book.count)
        db.delete(item)
        db.commit()
        return "ok"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="trust not found")

def get_trusts(db):
    return db.query(Trust).all()


def get_by_bookid(book_id,db):
    item = db.query(Trust).where(book_id==Trust.book_id).first()
    if not db.query(Book).where(book_id==Book.id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found book")
    elif not item :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found trust")
    return item


