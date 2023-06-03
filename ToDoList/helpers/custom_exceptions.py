class UnexpectedLengthError(Exception):
    """Raised with the length is not in the expected range"""
    pass

class InvalidRequestParamsError(Exception):
    """Raised when the request does not contain valid parameters"""
    pass
