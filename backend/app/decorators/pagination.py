from marshmallow import Schema
from flask import request, jsonify
from app.classes.paginator import Paginator
#pagination decorator

def pagination(schema: Schema, per_page: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            page = request.args.get('page', None)

            response = func(*args, **kwargs)

            paginator = Paginator(response, per_page)

            if page is not None:
                response = paginator.page(int(page)).all()
            else:
                response = response.all()

            list_ = schema.dump(response)

            return jsonify({
                "count": paginator.count,
                "results": list_
            })

        return wrapper

    return decorator
