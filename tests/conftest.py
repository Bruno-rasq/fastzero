import pytest

from fastapi.testclient import TestClient

from fastzero.app import app
from fastzero.models import table_registry

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


@pytest.fixture()
def client():
  return TestClient(app)


@pytest.fixture()
def session():
  engine = create_engine('sqlite:///:memory:')
  table_registry.metadata.create_all(engine)

  #gerenciamento de contexto
  with Session(engine) as session:
    yield session

  table_registry.metadata.drop_all(engine)