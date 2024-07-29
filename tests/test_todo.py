from tests.conftest import TodoFactory

from fastzero.models import TodoState

from fastapi import status



def test_create_todo(client, token):
  response = client.post(
    '/todos/',
    headers={'Authorization': f'Bearer {token}'},
    json={
      'title': 'task test',
      'description': 'task description',
      'state': 'draft'
    }
  )
  assert response.json() == {
    'id': 1,
    'title': 'task test',
    'description': 'task description',
    'state': 'draft'
  }


def test_list_todos_should_return_five_todos(client, session, token, user):
  expected_todos = 5
  session.bulk_save_objects(TodoFactory.create_batch(expected_todos, user_id = user.id))
  session.commit()

  response = client.get(
    '/todos/',
    headers={'Authorization': f'Bearer {token}'}
  )

  assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_two_todos(client, session, token, user):
  expected_todos = 2
  session.bulk_save_objects(TodoFactory.create_batch(5, user_id = user.id))
  session.commit()

  response = client.get(
    '/todos/?offset=1&limit=2',
    headers={'Authorization': f'Bearer {token}'}
  )

  assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title_should_retuns_five_todos(client, session, token, user):
  expected_todos = 5
  session.bulk_save_objects(
    TodoFactory.create_batch(5, user_id = user.id, title='test todo 1')
  )
  session.commit()

  response = client.get(
    '/todos/?title=Test todo 1',
    headers={'Authorization': f'Bearer {token}'}
  )

  assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_description_should_retuns_five_todos(client, session, token, user):
  expected_todos = 5
  session.bulk_save_objects(
    TodoFactory.create_batch(5, user_id = user.id, description='description')
  )
  session.commit()

  response = client.get(
    '/todos/?description=desc',
    headers={'Authorization': f'Bearer {token}'}
  )

  assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_state_should_retuns_five_todos(client, session, token, user):
  expected_todos = 5
  session.bulk_save_objects(
    TodoFactory.create_batch(5, user_id = user.id, state=TodoState.draft)
  )
  session.commit()

  response = client.get(
    '/todos/?state=draft',
    headers={'Authorization': f'Bearer {token}'}
  )

  assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, token, user):
  todo = TodoFactory(user_id=user.id)
  session.add(todo)
  session.commit()
  session.refresh(todo)

  response = client.delete(
    f'/todos/{user.id}',
    headers={'Authorization': f'Bearer {token}'}
  )

  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {'message': 'Task has been deleted successfully.'}


def test_delete_todo_error(client, token):
  response = client.delete(
    f'/todos/{10}',
    headers={'Authorization': f'Bearer {token}'}
  )

  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == {'detail': 'task not found'}


def test_patch_todo_error(client, token):
  response = client.patch(
    f'/todos/{10}',
    json={},
    headers={'Authorization': f'Bearer {token}'}
  )

  assert response.status_code == status.HTTP_404_NOT_FOUND
  assert response.json() == {'detail': 'task not found'}


def test_patch_todo(session, client, token, user):
  todo = TodoFactory(user_id=user.id)
  session.add(todo)
  session.commit()

  response = client.patch(
    f'/todos/{user.id}',
    json={'title': 'update title'},
    headers={'Authorization': f'Bearer {token}'}
  )

  assert response.status_code == status.HTTP_200_OK
  assert response.json()['title'] == 'update title'