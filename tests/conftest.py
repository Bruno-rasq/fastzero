import pytest

from fastapi.testclient import TestClient

from fastzero.app import app
from fastzero.database import get_session
from fastzero.models import table_registry, User

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


@pytest.fixture()
def client(session):

  def get_session_override():
    return session

  with TestClient(app) as client:
    app.dependency_overrides[get_session] = get_session_override 
    yield client
    
  app.dependency_overrides.clear()



@pytest.fixture()
def session():
  engine = create_engine(
    'sqlite:///:memory:',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
  )
  table_registry.metadata.create_all(engine)

  #gerenciamento de contexto
  with Session(engine) as session:
    yield session

  table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
  user= User(username='test', email='test@test.com', password='testtest')
  
  session.add(user)
  session.commit()
  session.refresh(user)

  return user