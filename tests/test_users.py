import pytest
from fastapi import status
from fastzero.schemas import UserPublic


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


def test_update_wrong_user(client, user, token):
  response = client.put(
    f'/users/{user.id + 1}',
    headers={'Authorization': f'Bearer {token}'},
    json={
      'username': 'testUsername2',
      'email'   : 'test@test.com',
      'password': 'password',
      'id': user.id
    }
  )

  assert response.status_code == status.HTTP_403_FORBIDDEN
  assert response.json() == { 'detail': 'Not enough permission' }


def test_delete_user(client, user, token):
  response = client.delete(
    f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
  )

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == { 'message': 'user deleted!' }


def test_delete_wrong_user(client, user, token):
  response = client.delete(
    f'/users/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
  )

  assert response.status_code == status.HTTP_403_FORBIDDEN
  assert response.json() == { 'detail': 'Not enough permission' }


# TASKS

#@pytest.mark.skip(reason='desabilitei p endpoint GET com ID')
def test_read_user_by_id_status_404_not_found(client, user):
  response = client.get(f'/users/{user.id + 1}')

  assert response.status_code == status.HTTP_404_NOT_FOUND


#@pytest.mark.skip(reason='desabilitei p endpoint GET com ID')
def test_read_user_by_id(client, user): 
  user_schema = UserPublic.model_validate(user).model_dump()
  response = client.get(f'/users/{user.id}')

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == user_schema