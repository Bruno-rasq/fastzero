from fastapi import status


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
  assert response.json() == {
    'users': [
      {
        'username': 'testusername',
        'email'   : 'test@test.com',
        'id': 1
      }
    ]
  }


def test_read_user_by_id(client):
  response = client.get('/users/1')

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {
    'username': 'testusername',
    'email'   : 'test@test.com',
    'id': 1
  }


def test_read_user_by_id_status_404_not_found(client):
  response = client.get('/users/29')

  assert response.status_code == status.HTTP_404_NOT_FOUND
  

def test_update_user(client):
  response = client.put(
    '/users/1',
    json={
      'username': 'testUsername2',
      'email'   : 'test@test.com',
      'password': 'password',
      'id': 1
    }
  )

  assert response.json() == {
    'username': 'testUsername2',
    'email'   : 'test@test.com',
    'id': 1
  }


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


def test_delete_user(client):
  response = client.delete('/users/1')

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == { 'message': 'user deleted!' }


def test_delete_user_status_404_not_found(client):
  response = client.delete('/users/29')

  assert response.status_code == status.HTTP_404_NOT_FOUND 