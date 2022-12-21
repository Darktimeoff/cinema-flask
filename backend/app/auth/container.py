from app.user.container import user_service

from .service import AuthService

auth_service = AuthService(user_service)
