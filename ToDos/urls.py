from django.urls import path
from ToDos import views

urlpatterns = [
    path('health', views.health_check),
    path('home', views.home_page),
    path('create_todo_list', views.create_todo_list),
    path('update_todo_list', views.update_todo_list),
    path('delete_todo_list', views.delete_todo_list),
    path('task', views.Task.as_view()),
]
