"""This file contains methods/classes that handle the requests from
URLs and return a response"""

import typing as ty

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from ToDoList import config
from ToDoList.helpers import custom_exceptions as ce
from ToDoList.helpers import logger, validator

# pylint: disable=unused-argument

def health_check(request: WSGIRequest) -> HttpResponse:
    """Endpoint for health check"""
    return HttpResponse(True)

class Login(TemplateView):
    """Contains methods that handle login requests"""

    def get(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Returns Login page template"""
        return render(request, 'Users/login.html')

    def post(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Authenticates the login request"""
        # TODO: move the home.html to ToDos app and make it display lists
        return render(request, 'Users/home.html')

def signup(request):
    return render(request, 'Users/signup.html')

def logout(request):
    return render(request, 'Users/login.html')
