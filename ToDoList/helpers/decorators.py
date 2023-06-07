"""This file contains decorators for logging and auth"""

import functools
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
