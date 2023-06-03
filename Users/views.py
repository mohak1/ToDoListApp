"""This file contains methods/classes that handle the requests from
URLs and return a response"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# pylint: disable=unused-argument

def health_check(request: WSGIRequest) -> HttpResponse:
    """Endpoint for health check"""
    return HttpResponse(True)

def home(request):
    return render(request, 'Users/home.html')

def login(request):
    return render(request, 'Users/login.html')

def signup(request):
    return render(request, 'Users/signup.html')

def logout(request):
    return render(request, 'Users/login.html')
