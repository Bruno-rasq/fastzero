from fastzero.security import create_access_token, SECRET_KEY, ALGORITHM

from jwt import decode
from fastapi import status



def test_jwt():
  data = {'sub': 'test@test.com'}
  token = create_access_token(data)

  result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

  assert result['sub'] == data['sub']
  assert result['exp']

def test_jwt_invalid_token(client):
  response = client.delete(
    '/users/1', headers={'Authorization': 'Bearer token-invalid'}
  )

  assert response.status_code == status.HTTP_401_UNAUTHORIZED
  assert response.json() == {'detail': 'Could not validate credentials'}