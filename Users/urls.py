from django.urls import path
from Users import views

urlpatterns = [
    path('health', views.health_check),
    path('login', views.Login.as_view()),
    path('signup', views.Signup.as_view()),
    path('logout', views.logout),
]
