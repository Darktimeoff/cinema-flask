from flask import request
from app.classes.paginator import Paginator

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
