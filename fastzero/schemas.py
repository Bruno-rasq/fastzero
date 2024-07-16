from pydantic import BaseModel, EmailStr
from typing import List


class Message(BaseModel):
  message: str

class UserSchema(BaseModel):
  username: str
  email: EmailStr
  password: str

class UserBD(UserSchema):
  id: int

class UserPublic(BaseModel):
  id: int
  username: str
  email: EmailStr

class UserList(BaseModel):
  users: List[UserPublic]