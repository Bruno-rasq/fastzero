from fastapi import FastAPI, status, HTTPException, Depends

from fastzero.schemas import Message, UserSchema, UserPublic, UserList
from fastzero.models import User
from fastzero.database import get_session

from sqlalchemy import select
from sqlalchemy.orm import Session



app = FastAPI()



@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def root_route():
  return { "message": "ok!" }


@app.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session=Depends(get_session)):
    
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
      
  db_user = User(username=user.username, email=user.email, password=user.password)

  session.add(db_user)
  session.commit()
  session.refresh(db_user)
    
  return db_user


@app.get('/users/', response_model=UserList)
def read_user(
  limit: int = 10,
  offset: int = 0,
  session: Session=Depends(get_session)
):
  users = session.scalars(select(User).limit(limit).offset(offset))
  return { 'users': users }




@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session=Depends(get_session)):

  db_user = session.scalar(select(User).where(User.id == user_id))

  if not db_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User not found!'
    )

  db_user.email = user.email
  db_user.password = user.password
  db_user.username = user.username

  session.commit()
  session.refresh(db_user)

  return db_user
  


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session=Depends(get_session)):

  db_user = session.scalar(select(User).where(User.id == user_id))

  if not db_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User not found!'
    )

  session.delete(db_user)
  session.commit()

  return { 'message': 'user deleted!' }




# TASK

@app.get('/users/{user_id}', response_model=UserPublic)
def get_user_by_id(user_id: int, session: Session=Depends(get_session)):
  db_user = session.scalar(select(User).where(User.id == user_id))

  if not db_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User not found'
    )

  return db_user