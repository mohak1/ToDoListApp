from django.db import models

from ToDoList import config

# pylint: disable=missing-class-docstring

class Userdb(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=config.MAX_NAME_LENGTH)
    last_name = models.CharField(max_length=config.MAX_NAME_LENGTH)
    email = models.CharField(unique=True, max_length=config.MAX_EMAIL_LENGTH)
    password = models.CharField(max_length=config.MAX_PASSWORD_LENGTH)
