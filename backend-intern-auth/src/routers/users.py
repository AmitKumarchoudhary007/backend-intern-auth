from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from .. import models, auth


router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: str
    name: str | None = None
    password: str



class LoginIn(BaseModel):
    email: str
    password: str



    

@router.post("/register")
def register(payload: RegisterIn, db: Session = Depends(auth.get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = models.User(
        email=payload.email,
        name=payload.name,
        hashed_password=auth.get_password_hash(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = auth.create_access_token(str(user.user_id))
    return {"access_token": token, "token_type": "bearer", "user_id": user.user_id}




@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not user.hashed_password or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = auth.create_access_token(str(user.user_id))
    return {"access_token": token, "token_type": "bearer"}
