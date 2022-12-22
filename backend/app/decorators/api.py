from flask import request
from app.classes.paginator import Paginator
from app.exceptions.http import ForbidenError
from app.utils.security import decode_jwt
from app.user.dao import UserDAO
from app.setup.db import db
from app.models import User

def serialized(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
      
            return schema.dump(response)
        return wrapper
    return decorator

def pagination(per_page: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            page = request.args.get('page', None)

            response = func(*args, **kwargs)

            paginator = Paginator(response, per_page)

            if page is not None:
                response = paginator.page(int(page)).all()
            else:
                response = response.all()

            return response

        return wrapper

    return decorator

def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            raise ForbidenError(message='Unauthorized', status_code=1)

        token = request.headers.get('Authorization').split(' ')[-1]
        try:
            data = decode_jwt(token)
            print('data', data['id'])
            user_dao = UserDAO(User, db)

            user = user_dao.get_by_id(data['id'])
            
            if not user:
                raise ForbidenError(message='Unauthorized', status_code=2)
        except Exception as e:
            print('err', e)
            raise ForbidenError(message='Unauthorized', status_code=3)
        else:
            return func(user=user, *args, **kwargs)
    
    return wrapper