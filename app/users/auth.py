from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.users.dao import UserDAO
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def get_password_hash(password: str)-> str:
  return pwd_context.hash(password)

def verify_password(plain_password, hashed_password)-> bool:
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict)->str:
  to_encode=data.copy()
  expire = datetime.now(timezone.utc)  + timedelta(minutes=30)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(
    to_encode, settings.SECRET_KEY, settings.SECRET_ALGORITHM
  )
  return encoded_jwt

async def authencicate_user(email: EmailStr, password: str):
  try:
    user = await UserDAO.find_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
      return None
    return user
  except:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
