from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import func, ForeignKey

from datetime import datetime
from enum import Enum

table_registry = registry()

class TodoState(str, Enum):
  draft = 'draft'
  todo  = 'todo'
  doing = 'doing'
  done  = 'done'
  trash = 'trash'


@table_registry.mapped_as_dataclass
class User:
  __tablename__ = 'users'
  
  id:         Mapped[int] = mapped_column(init=False, primary_key=True)
  username:   Mapped[str] = mapped_column()
  password:   Mapped[str] = mapped_column()
  email:      Mapped[str] = mapped_column(unique=True)
  created_at: Mapped[datetime] = mapped_column(
    init=False, server_default=func.now()
  )

@table_registry.mapped_as_dataclass
class Todo:
  __tablename__ = 'todos'

  id:          Mapped[int] = mapped_column(init=False, primary_key=True)
  title:       Mapped[str] = mapped_column()
  description: Mapped[str] = mapped_column()
  state:       Mapped[TodoState] = mapped_column()

  #toda list pertence a alguem
  user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))