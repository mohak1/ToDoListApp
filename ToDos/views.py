"""This file contains methods/classes that handle the requests from
URLs and return a response"""

import typing as ty

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from ToDoList import config
from ToDoList.helpers import custom_exceptions as ce
from ToDoList.helpers import db_operations as db_op
from ToDoList.helpers import decorators, logger, validator

# pylint: disable=unused-argument

@decorators.log_method
def health_check(request: WSGIRequest) -> HttpResponse:
    """Endpoint for health check"""
    return HttpResponse(True)


@require_http_methods(['GET'])
@decorators.log_method
@decorators.auth_required
def home_page(request: WSGIRequest) -> HttpResponse:
    msg = f'Logged in as {request.session["user"]["email"]}'
    todos = db_op.get_todo_lists_for_user(request.session.get('user')['id'])
    return render(request, 'ToDos/home.html',
                  context={'msg': msg, 'todos': todos})


@require_http_methods(['POST'])
@decorators.log_method
@decorators.auth_required
def create_todo_list(request: WSGIRequest, *args, **kwargs) -> ty.Any:
    """Adds a new ToDo List for the user"""
    try:
        validator.check_required_params(
            params=request.POST, required=['List Name']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.HOME_PAGE, context={'err': str(err)})

    list_name = request.POST.get('List Name')
    user_id = request.session.get('user')['id']

    try:
        validator.check_todo_list_name_length(list_name)
    except ce.UnexpectedLengthError as err:
        logger.log.error('Error: %s', str(err), exc_info=False)
        logger.log.debug('Error: %s', str(err), exc_info=True)
        return render(request, config.HOME_PAGE, context={'err': str(err)})

    db_op.create_new_todo_list(user_id, list_name)

    return redirect(config.HOME_REDIRECT_URL)


@require_http_methods(['POST'])
@decorators.log_method
@decorators.auth_required
def update_todo_list(request: WSGIRequest, *args, **kwargs) -> ty.Any:
    """Updates the selected ToDo List for the user"""
    try:
        validator.check_required_params(
            params=request.POST, required=['New Name', 'id']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.HOME_PAGE, context={'err': str(err)})

    new_name = request.POST.get('New Name')
    list_id = request.POST.get('id')
    user_id = request.session.get('user')['id']
    db_op.update_todo_list_name(user_id, list_id, new_name)
    return redirect(config.HOME_REDIRECT_URL)


@require_http_methods(['POST'])
@decorators.log_method
@decorators.auth_required
def delete_todo_list(request: WSGIRequest, *args, **kwargs) -> ty.Any:
    """Deletes the selected ToDo List for the user"""
    try:
        validator.check_required_params(params=request.POST, required=['id'])
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.HOME_PAGE, context={'err': str(err)})

    list_id = request.POST.get('id')
    user_id = request.session.get('user')['id']
    db_op.delete_todo_list_object(user_id, list_id)

    return redirect(config.HOME_REDIRECT_URL)


@method_decorator(decorators.auth_required, name='dispatch')
@method_decorator(decorators.log_method, name='dispatch')
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
