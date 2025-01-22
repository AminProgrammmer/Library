from fastapi import APIRouter,Depends,status
from sqlalchemy.orm.session import Session
from fastapi.exceptions import HTTPException
import pw_hash
from db.db_user import User
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from auth import auth2
from db.db import get_db

router = APIRouter(tags=['authentication'])


@router.post("/token")
def get_token(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(User).where(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "invalid credential")
    
    if not pw_hash.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "invalid password")

    access_token = auth2.create_access_token(data={"sub":request.username})
    
    return {
        "access_token":access_token,
        "type_token":"bearer",
        "user_id": user.id,
        "username" : user.username
    }

class RoleChecker:
    def __init__(self,allowed_roles):
        self.allowed_roles = allowed_roles
        
    def __call__(self,user:User=Depends(auth2.get_current_user)):
        if user.is_admin in self.allowed_roles:
            return user
        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you dont have enough permissions")