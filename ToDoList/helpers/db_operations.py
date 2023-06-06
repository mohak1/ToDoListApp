from django.http.request import QueryDict

from ToDoList.helpers import auth_operations as auth_op
from Users.models import Userdb
from ToDos.models import ToDoList, Task
from ToDoList.helpers import custom_exceptions as ce
from ToDoList import config


def create_new_user(params: QueryDict) -> None:
    """
    Creates a new entry in Userdb
    Raises `IntegrityError` if Email already exists
    """
    obj = Userdb()
    obj.first_name = params.get('FirstName')
    obj.last_name = params.get('LastName')
    obj.email = params.get('Email')
    obj.password = auth_op.get_hash(params.get('Password'))
    obj.save()

def get_user_from_login_cred(email: str, passw: str) -> Userdb:
    """
    Looks for an entry in Userdb that corresponds with the email and
    password pair.
    Raises `ce.NotFoundInDBError` if no entry is found
    """
    try:
        return Userdb.objects.get(email=email, password=passw)
    except Userdb.DoesNotExist as err:
        raise ce.NotFoundInDBError(config.LOGIN_FAIL_MESSAGE) from err

def get_user_obj_from_id(user_id: str):
    try:
        return Userdb.objects.get(id=user_id)
    except Userdb.DoesNotExist as err:
        raise ce.NotFoundInDBError('user_id not found in db') from err

def create_new_todo_list(user_id: str, list_name: str) -> None:
    """Creates a new entry in ToDoList db"""
    obj = ToDoList()
    obj.user = get_user_obj_from_id(user_id)
    obj.list_name = list_name
    obj.save()

def get_todo_list_obj_from_id(todo_list_id: str):
    try:
        return ToDoList.objects.get(id=todo_list_id)
    except ToDoList.DoesNotExist as err:
        raise ce.NotFoundInDBError('todo_list_id not found in db') from err

def update_todo_list_name(user_id: str, list_id: str, list_name: str) -> None:
    """Updates the name of the ToDoList"""
    obj = get_todo_list_obj_from_id(list_id)
    if obj.list_name != list_name and obj.user.id == user_id:
        obj.list_name = list_name
        obj.save()

def get_todo_lists_for_user(user_id: str):
    return ToDoList.objects.filter(user_id=user_id)

def get_tasks_of_todo_list(todo_list_id: str):
    return Task.objects.filter(list_id=todo_list_id)

def delete_todo_list_object(user_id: str, todo_list_id: str) -> None:
    obj = get_todo_list_obj_from_id(todo_list_id)
    if obj.user.id == user_id:
        obj.delete()
