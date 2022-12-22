import pytest
from app.user.dao import UserDAO
from unittest.mock import Mock
from app.models import User

@pytest.fixture(autouse=True)
def user_dao():
    user_dao = UserDAO(None, None)

    user1 = User(id=1, email="test@test.com", password="dc3khc7ThHEFQ6lBRvfk7W04URYH8eG5BpoD6M/orJM=")

    def update(id,data):
        for key, value in data.items():
            setattr(user1, key, value)

        return user1

    user_dao.get_by_id = Mock(return_value=user1)
    user_dao.get_by_email = Mock(return_value=user1)
    user_dao.create  = lambda data: User(**data)
    user_dao.delete  = Mock(return_value=user1)
    user_dao.update = update

    return user_dao

