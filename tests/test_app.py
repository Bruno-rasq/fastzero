import pytest
from fastapi import status

from fastzero.schemas import UserPublic


def test_root_deve_retornar_status_code_200_ok_e_OK(client):
  
  response = client.get('/') # act

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == { "message": "ok!" }


def test_create_user(client):

  response = client.post( #UserSchema
    '/users/',
    json={
      'username': 'testusername',
      'email'   : 'test@test.com',
      'password': 'password'
    }
  )

  #validar UserPublic
  assert response.status_code == status.HTTP_201_CREATED
  assert response.json() == {
    'username': 'testusername',
    'email'   : 'test@test.com',
    'id': 1
  }


def test_read_users(client):
  response = client.get('/users/')

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
  
  user_schema = UserPublic.model_validate(user).model_dump()
  response = client.get('/users/')

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
  response = client.put(
    f'/users/{user.id}',
    headers={'Authorization': f'Bearer {token}'},
    json={
      'username': 'testUsername2',
      'email'   : 'test@test.com',
      'password': 'password',
      'id': user.id
    }
  )

  assert response.json() == {
    'username': 'testUsername2',
    'email'   : 'test@test.com',
    'id': user.id
  }


def test_delete_user(client, user, token):
  response = client.delete(
    f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
  )

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == { 'message': 'user deleted!' }


def test_get_token(client, user):
  response = client.post(
    '/token',
    data={ 'username': user.email, 'password': user.clean_password }
  )
  
  token = response.json()

  assert response.status_code == status.HTTP_200_OK
  assert token['token_type'] == 'Bearer'
  assert 'access_token' in token

  


# TASK 

@pytest.mark.skip(reason='Adicionar o token deixa o teste sem sentido')
def test_delete_user_status_404_not_found(client):
  response = client.delete('/users/29')

  assert response.status_code == status.HTTP_404_NOT_FOUND 


@pytest.mark.skip(reason='Adicionar o token deixa o teste sem sentido')
def test_update_user_status_404_not_found(client):
  response = client.put(
    '/users/29',
    json={
      'username': 'testUsername2',
      'email'   : 'test@test.com',
      'password': 'password',
      'id': 29
    }
  )

  assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.skip(reason='desabilitei p endpoint GET com ID')
def test_read_user_by_id_status_404_not_found(client):
  response = client.get('/users/29')

  assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.skip(reason='desabilitei p endpoint GET com ID')
def test_read_user_by_id(client, user): #TASK corrigir
  user_schema = UserPublic.model_validate(user).model_dump()
  response = client.get('/users/1')

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == user_schema