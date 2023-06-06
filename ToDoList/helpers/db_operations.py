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

def update_todo_list_name(list_id: str, list_name: str) -> None:
    """Updates the name of the ToDoList"""
    obj = get_todo_list_obj_from_id(list_id)
    if obj.list_name != list_name: # save the name if it's different
        obj.list_name = list_name
        obj.save()

def get_todo_lists_for_user(user_id: str):
    return ToDoList.objects.filter(user_id=user_id)

def delete_todo_list_object(todo_list_id: str) -> None:
    obj = get_todo_list_obj_from_id(todo_list_id)
    obj.delete()

def get_tasks_of_todo_list(todo_list_id: str):
    return Task.objects.filter(todo_list_id=todo_list_id)

def create_new_task(todo_list_id: str, task_value: str) -> None:
    """Creates a new entry in ToDoList db"""
    obj = Task()
    obj.todo_list = get_todo_list_obj_from_id(todo_list_id)
    obj.task_value = task_value
    obj.save()

def get_task(todo_list_id: str, task_id: str):
    try:
        return Task.objects.get(id=task_id, todo_list=todo_list_id)
    except Task.DoesNotExist as err:
        raise ce.NotFoundInDBError('todo_list_id not found in db') from err

def update_task_value(todo_list_id: str, task_id: str, new_val: str):
    obj = get_task(todo_list_id, task_id)
    if obj.task_value != new_val:
        obj.task_value = new_val
        obj.save()

def delete_task_object(todo_list_id: str, task_id: str):
    obj = get_task(todo_list_id, task_id)
    obj.delete()

def toggle_completed_value(todo_list_id: str, task_id: str):
    obj = get_task(todo_list_id, task_id)
    obj.completed = not obj.completed
    obj.save()
