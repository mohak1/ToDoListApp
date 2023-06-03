from django.urls import path
from ToDos import views

urlpatterns = [
    path('health', views.health_check),
]
