from django.urls import path
from ToDos import views

urlpatterns = [
    path('health', views.health_check),
    path('home', views.home_page),
    path('todolist', views.ToDoList.as_view()),
    path('task', views.Task.as_view()),
]
