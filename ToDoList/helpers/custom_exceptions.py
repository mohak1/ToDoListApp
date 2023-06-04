class UnexpectedLengthError(Exception):
    """Raised with the length is not in the expected range"""
    pass

class InvalidRequestParamsError(Exception):
    """Raised when the request does not contain valid parameters"""
    pass

class NotFoundInDBError(Exception):
    """Raised when a database qurey returns no matches"""
    pass
