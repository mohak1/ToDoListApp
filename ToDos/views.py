"""This file contains methods/classes that handle the requests from
URLs and return a response"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect

# pylint: disable=unused-argument

def health_check(request: WSGIRequest) -> HttpResponse:
    """Endpoint for health check"""
    return HttpResponse(True)

def home_page(request: WSGIRequest) -> HttpResponse:
    msg = f'Logged in as {request.session["user"]["email"]}'
    return render(request, 'ToDos/home.html', context={'msg': msg})
