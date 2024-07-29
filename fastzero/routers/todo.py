from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Annotated

from fastzero.schemas import TodoSchema, TodoPublic, TodoList, Message, TodoUpdate
from fastzero.database import get_session
from fastzero.security import get_current_user
from fastzero.models import TodoState, User, Todo



router = APIRouter(prefix='/todos', tags=['todo'])


T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User,Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(todo: TodoSchema, session: T_Session, user: CurrentUser):
  db_todo = Todo(
    title       = todo.title,
    description = todo.description,
    state       = todo.state,
    user_id     = user.id
  )
  session.add(db_todo)
  session.commit()
  session.refresh(db_todo)
  return db_todo


@router.get('/', response_model=TodoList)
def list_todos(
  session:     T_Session, 
  user:        CurrentUser,
  state:       TodoState | None = None,
  title:       str | None = None,
  description: str | None = None,
  offset:      int | None = None,
  limit:       int | None = None
):
  query = select(Todo).where(Todo.user_id == user.id)

  if title:
    query = query.filter(Todo.title.contains(title))

  if description:
    query = query.filter(Todo.description.contains(description))

  if state:
    query = query.filter(Todo.state == state)

  todos = session.scalars(query.offset(offset).limit(limit)).all()

  return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: CurrentUser):
  todo = session.scalar(select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id))

  if not todo:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='task not found'
    )

  session.delete(todo)
  session.commit()

  return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=TodoUpdate)
def patch_todo(todo_id: int, session: T_Session, user: CurrentUser, todo: TodoUpdate):
  db_todo = session.scalar(
    select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
  )

  if not db_todo:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail='task not found'
    )

  for key, value in todo.model_dump(exclude_unset=True).items():
    setattr(db_todo, key, value)

  session.add(db_todo)
  session.commit()
  session.refresh(db_todo)

  return db_todo