from fastapi import FastAPI, status, HTTPException

from fastzero.schemas import Message, UserSchema, UserPublic, UserBD, UserList


app = FastAPI()

database = [] # fake db


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def root_route():
  return { "message": "ok!" }


# CRUD

@app.post('/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
  
  user_with_id = UserBD(
    id=len(database) + 1,
    **user.model_dump()
  )

  database.append(user_with_id)
  
  return user_with_id


@app.get('/users/', response_model=UserList)
def read_user():
  return { 'users': database }


@app.get('/users/{user_id}', response_model=UserPublic)
def get_user_by_id(user_id: int):
  if user_id < 1 or user_id > len(database) + 1:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail='User not found'
    )

  user = database[user_id - 1]
  return user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):

  if user_id < 1 or user_id > len(database) + 1:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail='User not found'
    )
    
  user_with_id = UserBD(**user.model_dump(), id=user_id)
  
  database[user_id - 1] = user_with_id
  
  return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
  if user_id < 1 or user_id > len(database) + 1:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail='User not found'
    )

  del database[user_id - 1]

  return { 'message': 'user deleted!' }