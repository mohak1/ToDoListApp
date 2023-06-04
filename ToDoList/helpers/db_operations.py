from django.http.request import QueryDict

from ToDoList.helpers import auth_operations as auth_op
from Users import models
from ToDoList.helpers import custom_exceptions as ce
from ToDoList import config


def create_new_user(params: QueryDict) -> None:
    obj = models.Userdb()
    obj.first_name = params.get('First Name')
    obj.last_name = params.get('Last Name')
    obj.email = params.get('Email')
    obj.password = auth_op.get_hash(params.get('Password'))
    obj.save()

def get_user_from_login_cred(email: str, passw: str) -> models.Userdb:
    try:
        return models.Userdb.objects.get(email=email, password=passw)
    except models.Userdb.DoesNotExist as err:
        raise ce.NotFoundInDBError(config.LOGIN_FAIL_MESSAGE) from err
