from fastapi import status
from freezegun import freeze_time


def test_get_token(client, user):
  response = client.post(
    '/auth/token',
    data={ 'username': user.email, 'password': user.clean_password }
  )

  token = response.json()

  assert response.status_code == status.HTTP_200_OK
  assert token['token_type'] == 'Bearer'
  assert 'access_token' in token


def test_token_exoired_after_time(client, user):
  with freeze_time('2024-07-23 12:00:00'):
    #gera o token (12:00)
    response = client.post(
      '/auth/token',
      data={'username': user.email, 'password': user.clean_password}
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()['access_token']

  with freeze_time('2024-07-23 12:31:00'):
    #usa o token (12:31)
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
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == { 'detail':'Could not validate credentials' }


def test_token_wrong_password(client, user):
  response = client.post(
    '/auth/token',
    data={'username': user.email, 'password': 'wrong_password'}
  )
  assert response.status_code == status.HTTP_400_BAD_REQUEST
  assert response.json() == { 'detail':'Incorrect email or password' }


def test_token_wrong_email(client, user):
  response = client.post(
    '/auth/token',
    data={'username': 'wrong@email.com', 'password': user.clean_password}
  )
  assert response.status_code == status.HTTP_400_BAD_REQUEST
  assert response.json() == { 'detail':'Incorrect email or password' }


def test_refresh_token(client, user, token):
  response = client.post(
    '/auth/refresh_token',
    headers={'Authorization': f'Bearer {token}'}
  )
  
  data = response.json()
  assert response.status_code == status.HTTP_200_OK
  assert 'access_token' in data
  assert 'token_type' in data
  assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user):
  with freeze_time('2023-07-14 12:00:00'):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()['access_token']

  with freeze_time('2023-07-14 12:31:00'):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}