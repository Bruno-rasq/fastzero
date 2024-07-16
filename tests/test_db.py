from sqlalchemy import select
from fastzero.models import User


def test_create_user(session):
  
  user = User(username='testname', email='mail@mail.com', password='batatinha')

  session.add(user)
  session.commit()
  
  result = session.scalar(select(User).where(User.email == 'mail@mail.com'))

  assert result.id == 1