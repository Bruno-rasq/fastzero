from fastapi import status


def test_root_deve_retornar_status_code_200_ok_e_OK(client):
  
  response = client.get('/') # act

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == { "message": "ok!" }