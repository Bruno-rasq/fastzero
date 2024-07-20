from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastzero.schemas import Message, UserSchema, UserPublic, UserList, Token
from fastzero.models import User
from fastzero.database import get_session
from fastzero.security import get_password_hash, verify_password, create_access_token, get_current_user

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
      
  db_user = User(
    username=user.username, 
    email=user.email, 
    password=get_password_hash(user.password)
  )

  session.add(db_user)
  session.commit()
  session.refresh(db_user)
    
  return db_user


@app.get('/users/', response_model=UserList)
def read_user(
  limit: int = 10, offset: int = 0,
  session: Session=Depends(get_session)
):
  users = session.scalars(select(User).limit(limit).offset(offset))
  return { 'users': users }


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
  user_id: int, 
  user: UserSchema, 
  session: Session=Depends(get_session),
  current_user= Depends(get_current_user)
):
  if current_user.id != user_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail='Not enough permission'
    )
    
  current_user.email = user.email
  current_user.password = get_password_hash(user.password)
  current_user.username = user.username

  session.commit()
  session.refresh(current_user)

  return current_user
  


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
  user_id: int, 
  session: Session=Depends(get_session),
  current_user= Depends(get_current_user)
):

  if current_user.id != user_id:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST, 
      detail='Not enough permission'
    )
    
  session.delete(current_user)
  session.commit()

  return { 'message': 'user deleted!' }





@app.post('/token', response_model=Token)
def login_for_access_token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  session: Session = Depends(get_session)
):
  user = session.scalar(select(User).where(User.email == form_data.username))

  if not user or not verify_password(form_data.password, user.password):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail= 'Incorrect email or passowrd'
    )
  access_token = create_access_token(data={'sub': user.email})

  return {'access_token': access_token, 'token_type': 'Bearer'}



# TASK - Arrumar o endpoint GET com ID
@app.get('/users/{user_id}', response_model=UserPublic)
def get_user_by_id(user_id: int, session: Session=Depends(get_session)):
  db_user = session.scalar(select(User).where(User.id == user_id))

  if not db_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='User not found'
    )

  return db_user