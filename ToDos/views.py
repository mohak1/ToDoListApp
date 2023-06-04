"""This file contains methods/classes that handle the requests from
URLs and return a response"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
import typing as ty

# pylint: disable=unused-argument

def health_check(request: WSGIRequest) -> HttpResponse:
    """Endpoint for health check"""
    return HttpResponse(True)

def home_page(request: WSGIRequest) -> HttpResponse:
    msg = f'Logged in as {request.session["user"]["email"]}'
    return render(request, 'ToDos/home.html', context={'msg': msg})


class ToDoList(TemplateView):
    """Contains methods that handle ToDo List requests"""

    def get(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Returns all the ToDo Lists of the user"""
        ...

    def post(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Adds a new ToDo List for the user"""
        ...

    def put(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Updates the selected ToDo List for the user"""
        ...

    def delete(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Deletes the selected ToDo List for the user"""
        ...


class Task(TemplateView):
    """Contains methods that handle task requests"""

    def get(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Returns all the Tasks of the specified ToDo List"""
        ...

    def post(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Adds a new Task to the specified ToDo List"""
        ...

    def put(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Updates the selected Task in the ToDo List"""
        ...

    def delete(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Deletes the selected Task from the ToDo List"""
        ...
