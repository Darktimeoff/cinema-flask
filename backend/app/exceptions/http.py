class BasicHTTPError(Exception):
    code: int
    status_code: int = -1

    def __init__(self, message: str, code = 500, status_code: int = -1) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class InternalServerError(BasicHTTPError):
    code = 500

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(code=self.code, *args, **kwargs)


class NotFoundError(BasicHTTPError):
    code = 404

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(code=self.code, *args, **kwargs)

class BadRequestError(BasicHTTPError):
    code = 400

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(code=self.code, *args, **kwargs)