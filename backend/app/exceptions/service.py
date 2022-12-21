from .http import BadRequestError

class ValidationError(BadRequestError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UniqueError(BadRequestError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)