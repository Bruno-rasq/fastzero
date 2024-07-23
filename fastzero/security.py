from pwdlib import PasswordHash
from jwt import decode, encode
from jwt.exceptions import PyJWTError, ExpiredSignatureError

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy import select

from fastzero.database import get_session
from fastzero.models import User
from fastzero.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_sheme = OAuth2PasswordBearer(tokenUrl='auth/token')

settings = Settings()

def get_password_hash(password: str):
  # gera a senha
  return pwd_context.hash(password) 


def verify_password(plain_password: str, hashed_password: str):
  # verficar se a senha limpa é igual a senha hashada
  return pwd_context.verify(plain_password, hashed_password) 


def create_access_token(data: dict):
  to_encode = data.copy()

  expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
  )

  to_encode.update({'exp': expire})
  encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
  
  return encoded_jwt


def get_current_user(
  session: Session = Depends(get_session),
  token: str = Depends(oauth2_sheme)
):
  credentials_exception = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
  )
  
  try:
    payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    username = payload.get('sub')
    if not username:
      raise credentials_exception
      
  except ExpiredSignatureError:
    raise credentials_exception
    
  except PyJWTError:
    raise credentials_exception
    
    
  user = session.scalar(select(User).where(User.email == username))

  if not user:
    raise credentials_exception

  return user