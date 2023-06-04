from django.http.request import QueryDict

from ToDoList.helpers import hasher
from Users import models


def create_new_user(params: QueryDict) -> None:
    obj = models.Userdb()
    obj.first_name = params.get('First Name')
    obj.last_name = params.get('Last Name')
    obj.email = params.get('Email')
    obj.password = hasher.get_hash(params.get('Password'))
    obj.save()
