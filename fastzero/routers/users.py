from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from sqlalchemy.orm import Session
from sqlalchemy import select

from fastzero.schemas import Message, UserSchema, UserPublic, UserList
from fastzero.security import get_current_user, get_password_hash
from fastzero.database import get_session
from fastzero.models import User


router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):

  db_user = session.scalar(
    select(User).where(
      (User.username == user.username) | (User.email == user.email)
    )
  )

  if db_user:
    if db_user.username == user.username:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='username already exists'
      )

    elif db_user.email == user.email:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='email already exists'
      )

  db_user = User(
    username=user.username, 
    email=user.email, 
    password=get_password_hash(user.password)
  )

  session.add(db_user)
  session.commit()
  session.refresh(db_user)

  return db_user


@router.get('/', response_model=UserList)
def read_user(session: T_Session, limit: int = 10, offset: int = 0):
  users = session.scalars(select(User).limit(limit).offset(offset))
  return { 'users': users }


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id:int, user:UserSchema, session:T_Session, current_user:T_CurrentUser):
  
  if current_user.id != user_id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN, 
      detail='Not enough permission'
    )

  current_user.email = user.email
  current_user.password = get_password_hash(user.password)
  current_user.username = user.username

  session.commit()
  session.refresh(current_user)

  return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: T_Session,current_user: T_CurrentUser):

  if current_user.id != user_id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN, 
      detail='Not enough permission'
    )

  session.delete(current_user)
  session.commit()

  return { 'message': 'user deleted!' }



# TASK - Arrumar o endpoint GET com ID
@router.get('/{user_id}', response_model=UserPublic)
def get_user_by_id(user_id: int, session: T_Session):
  db_user = session.scalar(select(User).where(User.id == user_id))

  if not db_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User not found'
    )

  return db_user