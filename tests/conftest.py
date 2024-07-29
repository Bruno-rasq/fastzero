import pytest
import factory
import factory.fuzzy

from fastapi.testclient import TestClient

from fastzero.app import app
from fastzero.database import get_session
from fastzero.models import Todo, TodoState, table_registry, User
from fastzero.security import get_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


#fabrica de meninos kk
class UserFactory(factory.Factory):
  class Meta:
    model = User

  username = factory.Sequence(lambda n: f'test{n}')
  email    = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
  password = factory.LazyAttribute(lambda obj: f'{obj.username}+senha')


class TodoFactory(factory.Factory):
  class Meta:
    model = Todo

  title = factory.Faker('text')
  description = factory.Faker('text')
  state = factory.fuzzy.FuzzyChoice(TodoState)
  user_id = 1

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

  pwd = 'testetest'
  user = UserFactory(
    password=get_password_hash(pwd)
  )
  
  session.add(user)
  session.commit()
  session.refresh(user)

  user.clean_password = pwd # monkey patch

  return user


@pytest.fixture()
def other_user(session):
  user = UserFactory()
  session.add(user)
  session.commit()
  session.refresh(user)


  return user


@pytest.fixture()
def token(client, user):
  response = client.post(
    '/auth/token',
    data={'username': user.email, 'password': user.clean_password}
  )
  return response.json()['access_token']