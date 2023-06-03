"""This file contains methods/classes that handle the requests from
URLs and return a response"""

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

# pylint: disable=unused-argument

def health_check(request: WSGIRequest) -> HttpResponse:
    """Endpoint for health check"""
    return HttpResponse(True)
