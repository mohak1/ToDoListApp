from django.urls import path
from ToDos import views

urlpatterns = [
    path('health', views.health_check),
    path('todo_lists', views.todo_list_page),
    path('tasks/<int:todo_list_id>', views.tasks_page),
    path('create_todo_list', views.create_todo_list),
    path('update_todo_list', views.update_todo_list),
    path('delete_todo_list', views.delete_todo_list),
    path('get_tasks/<int:todo_list_id>', views.get_tasks),
    path('create_task', views.create_task),
    path('update_task', views.update_task),
    path('delete_task', views.delete_task),
    path('toggle_task_status', views.toggle_task_status),
]
