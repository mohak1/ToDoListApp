from django.contrib import admin
from ToDos import models

admin.site.register(models.ToDoList)
admin.site.register(models.Task)
