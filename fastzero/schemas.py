from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List

from fastzero.models import TodoState

class Message(BaseModel):
  message: str


class UserSchema(BaseModel):
  username: str
  email:    EmailStr
  password: str


class UserPublic(BaseModel):
  id:       int
  username: str
  email:    EmailStr
  model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
  users: List[UserPublic]


class Token(BaseModel):
  access_token: str
  token_type:   str


class TodoSchema(BaseModel):
  title:       str
  description: str
  state:       TodoState


class TodoPublic(TodoSchema):
  id: int


class TodoList(BaseModel):
  todos: List[TodoPublic]


class TodoUpdate(BaseModel):
  title:       str | None = None
  description: str | None = None
  state:       TodoState | None = None