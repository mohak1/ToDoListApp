"""This file contains decorators for logging and auth"""

import functools

from django.http import HttpResponseBadRequest
from ToDoList import config
from ToDoList.helpers import custom_exceptions as ce
from ToDoList.helpers import logger
from django.shortcuts import redirect


def log_method(func):
    """
    This decorator logs the entry and exit of a method on INFO level
    Also logs the arguments and result values on DEBUG level
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        method_name = func.__name__
        logger.log.info('Entering function: `%s`', method_name)
        logger.log.debug('with args: %s, kwargs: %s', args, kwargs)
        result = func(*args, **kwargs)
        logger.log.info('`%s` executed.', method_name)
        logger.log.debug('result: %s', result)
        return result
    return wrapper

def auth_required(func):
    """
    This decorator checks if the incoming request is authenticated by
    looking for 'user' key in the request session dictionary.
    If the request is not authenticated, the redirect to the login
    page is returned
    """
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user'):
            return redirect(config.LOGIN_REDIRECT_URL)
        result = func(request, *args, **kwargs)
        return result
    return wrapper

def params_required(required_param_dict):
    """
    This decorator checks if the incoming request has the params
    necessary for the processing. This check is done by checking if
    the required parameters are a subset of the parameters in the
    incomming request. 
    Returns a status code 400 response if params are missing
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            for key in required_param_dict:
                if key.upper() == 'GET':
                    request_params = set(request.GET.keys())
                    required_params = set(required_param_dict['POST'])
                    if not required_params.issubset(request_params):
                        response = HttpResponseBadRequest()
                        return response
                if key.upper() == 'POST':
                    request_params = set(request.POST.keys())
                    required_params = set(required_param_dict['POST'])
                    if not required_params.issubset(request_params):
                        response = HttpResponseBadRequest()
                        return response
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
