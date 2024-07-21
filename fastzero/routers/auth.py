from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.schemas import Token
from fastzero.models import User
from fastzero.database import get_session
from fastzero.security import create_access_token, verify_password


router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login_for_access_token(session: T_Session,form_data: T_OAuthForm):
  
  user = session.scalar(select(User).where(User.email == form_data.username))

  if not user or not verify_password(form_data.password, user.password):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail= 'Incorrect email or passowrd'
    )
  access_token = create_access_token(data={'sub': user.email})

  return {'access_token': access_token, 'token_type': 'Bearer'}