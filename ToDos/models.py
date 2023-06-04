from django.db import models
from Users.models import Userdb
from ToDoList import config

# pylint: disable=missing-class-docstring

class ToDoList(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(Userdb, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=config.MAX_LIST_NAME_LENGTH)

class Task(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    task_value = models.CharField(max_length=config.MAX_TASK_VALUE_LENGTH)
    completed = models.BooleanField(default=False)
