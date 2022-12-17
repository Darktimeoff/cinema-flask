class BasicHTTPError(Exception):
    code: int


class InternalServerError(BasicHTTPError):
    code = 500


class NotFoundError(BasicHTTPError):
    code = 404

class BadRequestError(BasicHTTPError):
    code = 400