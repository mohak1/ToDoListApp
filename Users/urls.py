from django.urls import path
from Users import views

urlpatterns = [
    path('health', views.health_check),
    path('home', views.home),
    path('login', views.login),
    path('signup', views.signup),
    path('logout', views.logout),
]
