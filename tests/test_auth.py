from fastapi import status


def test_get_token(client, user):
  response = client.post(
    '/auth/token',
    data={ 'username': user.email, 'password': user.clean_password }
  )

  token = response.json()

  assert response.status_code == status.HTTP_200_OK
  assert token['token_type'] == 'Bearer'
  assert 'access_token' in token
