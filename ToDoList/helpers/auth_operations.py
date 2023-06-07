from django.contrib.auth.hashers import make_password
from django.core.handlers.wsgi import WSGIRequest

from ToDoList import config
from ToDoList.helpers import custom_exceptions as ce
from ToDoList.helpers import db_operations as db_op
from ToDoList.helpers import decorators, logger


@decorators.log_method
def get_hash(password: str) -> str:
    """Returns a hashed string of the input string"""
    return make_password(password, salt=config.SALT)

@decorators.log_method
def authenticate_login(request: WSGIRequest) -> None:
    """
    Checks if the `Email` and `Password` in the request exist in the db
    and sets the user details in the request session
    Raises `ce.NotFoundInDBError` if no entries are found in the db
    that match the provided email and hashed password
    """
    email = request.POST.get('Email')
    passw = get_hash(request.POST.get('Password'))
    try:
        user_obj = db_op.get_user_from_login_cred(email, passw)
    except ce.NotFoundInDBError as err:
        logger.log.error('Error: %s', str(err))
        raise
    request.session['user'] = {
        'id': user_obj.id, 'fname': user_obj.first_name,
        'email': user_obj.email}
