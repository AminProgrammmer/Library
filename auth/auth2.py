from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from db.db import get_db
from datetime import datetime, timedelta
from jose import jwt , JWTError
from typing import Optional
from db.db_user import read_user_username
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = '6c7d438d2ea66cc11ee315566bda6f45336930dc2a40eaa96ec009524c20aa69'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()
    if expires_delta:
      expire = datetime.utcnow() + expires_delta
    else:
      expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    error_credential = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="invalid credentials",
      headers={"www-authenticate" : "bearer"}
    )
  
    try:
      _dict = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
      username = _dict.get("sub")
      if not username:
        raise error_credential
    except JWTError:
      raise error_credential
    
    user = read_user_username(username,db)
    
    return user