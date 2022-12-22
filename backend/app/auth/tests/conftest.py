import pytest
from app.user.service import UserService
from unittest.mock import Mock
from app.models import User
from app.utils.security import get_refresh_token
from app.container import user_schema
@pytest.fixture()
def user_service():
    user_service =  UserService(None)

    user_service.get_by_email = Mock()
    user_service.get_by_id = Mock()
    user_service.create = Mock()
    user_service.update = Mock()
    user_service.delete = Mock()
    user_service.generate_password = Mock()
    user_service.compare_password = Mock()

    return user_service

@pytest.fixture()
def user():
    user = User(id=1, email='test@example.com', password='test', refresh_token='asdsad')
    data = user_schema.dump(user)
    refresh_token = get_refresh_token(data)
    user.refresh_token = refresh_token
 
    return user