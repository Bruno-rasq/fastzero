from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List


class Message(BaseModel):
  message: str

class UserSchema(BaseModel):
  username: str
  email: EmailStr
  password: str


class UserPublic(BaseModel):
  id: int
  username: str
  email: EmailStr
  model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
  users: List[UserPublic]