"""This file contains methods/classes that handle the requests from
URLs and return a response"""

import typing as ty

from django.core.handlers.wsgi import WSGIRequest
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from ToDoList import config
from ToDoList.helpers import custom_exceptions as ce
from ToDoList.helpers import db_operations as db_op
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


class Signup(TemplateView):
    """Contains methods that handle signup requests"""

    def get(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Returns Signup page template"""
        return render(request, 'Users/signup.html')

    def post(self, request: WSGIRequest, *args, **kwargs) -> ty.Any:
        """Performs user signup and redirects to Login page"""

        try:
            validator.check_required_params(
                params=request.POST,
                required=['First Name', 'Last Name', 'Email',
                          'Password', 'Confirm Password'])
        except ce.InvalidRequestParamsError as err:
            logger.log.error('Error: %s', str(err))
            return render(request, config.SIGNUP_PAGE, context={'msg': str(err)})

        if request.POST.get('Password') != request.POST.get('Confirm Password'):
            msg = '`Password` and `Confirm Password` values are not same'
            return render(request, config.SIGNUP_PAGE, context={'msg': msg})

        try:
            validator.check_signup_params_length(request.POST)
        except ce.UnexpectedLengthError as err:
            logger.log.error('Error: %s', str(err), exc_info=False)
            logger.log.debug('Error: %s', str(err), exc_info=True)
            return render(request, config.SIGNUP_PAGE, context={'msg': str(err)})

        try:
            db_op.create_new_user(request.POST)
        except IntegrityError as err:
            msg = f'An account already exists with {request.POST.get("Email")}'
            logger.log.debug('Error: %s', str(err), exc_info=True)
            logger.log.error('Error: %s', str(msg), exc_info=False)
            return render(request, config.SIGNUP_PAGE, context={'msg': str(msg)})

        msg = config.SIGNUP_SUCCESS_MESSAGE
        return render(request, config.LOGIN_PAGE, context={'msg': msg})


def logout(request: WSGIRequest) -> ty.Any:
    """Logs out the user and redirects to Login page"""
    return render(request, 'Users/login.html')
