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
@decorators.auth_required
@decorators.log_method
def todo_list_page(request: WSGIRequest) -> HttpResponse:
    msg = f'Logged in as {request.session["user"]["email"]}'
    todos = db_op.get_todo_lists_for_user(request.session.get('user')['id'])
    return render(request, config.TODO_LISTS_PAGE,
                  context={'msg': msg, 'todos': todos})

@require_http_methods(['GET'])
@decorators.auth_required
@decorators.log_method
def tasks_page(request: WSGIRequest, todo_list_id: str) -> HttpResponse:
    msg = f'Logged in as {request.session["user"]["email"]}'
    tasks = db_op.get_tasks_of_todo_list(todo_list_id)
    return render(request, config.TASKS_PAGE,
                  context={'msg': msg, 'list_id': todo_list_id, 'tasks': tasks})

@require_http_methods(['POST'])
@decorators.auth_required
@decorators.log_method
def create_todo_list(request: WSGIRequest) -> ty.Any:
    """Adds a new ToDo List for the user"""
    try:
        validator.check_required_params(
            params=request.POST, required=['ListName']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.TODO_LISTS_PAGE, context={'err': str(err)})

    list_name = request.POST.get('ListName')
    user_id = request.session.get('user')['id']

    try:
        validator.check_todo_list_name_length(list_name)
    except ce.UnexpectedLengthError as err:
        logger.log.error('Error: %s', str(err), exc_info=False)
        logger.log.debug('Error: %s', str(err), exc_info=True)
        return render(request, config.TODO_LISTS_PAGE, context={'err': str(err)})

    db_op.create_new_todo_list(user_id, list_name)

    return redirect(config.TODO_LISTS_REDIRECT_URL)


@require_http_methods(['POST'])
@decorators.auth_required
@decorators.log_method
def update_todo_list(request: WSGIRequest) -> ty.Any:
    """Updates the selected ToDo List for the user"""
    try:
        validator.check_required_params(
            params=request.POST, required=['NewName', 'ToDoListID']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.TODO_LISTS_PAGE, context={'err': str(err)})

    new_name = request.POST.get('NewName')
    todo_list_id = request.POST.get('ToDoListID')
    db_op.update_todo_list_name(todo_list_id, new_name)
    return redirect(config.TODO_LISTS_REDIRECT_URL)


@require_http_methods(['POST'])
@decorators.auth_required
@decorators.log_method
def delete_todo_list(request: WSGIRequest) -> ty.Any:
    """Deletes the selected ToDo List for the user"""
    try:
        validator.check_required_params(params=request.POST, required=['ToDoListID'])
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.TODO_LISTS_PAGE, context={'err': str(err)})

    todo_list_id = request.POST.get('ToDoListID')
    db_op.delete_todo_list_object(todo_list_id)

    return redirect(config.TODO_LISTS_REDIRECT_URL)


@require_http_methods(['GET'])
@decorators.auth_required
@decorators.log_method
def get_tasks(request: WSGIRequest, todo_list_id: str) -> ty.Any:
    """Returns all the Tasks of the specified ToDo List"""

    list_name = 'Name Of The List'
    tasks = db_op.get_tasks_of_todo_list(todo_list_id)
    msg = f'Logged in as {request.session["user"]["email"]}'
    return render(request, config.TASKS_PAGE,
                  context={
                      'msg': msg, 'list_name': list_name,
                      'tasks': tasks, 'list_id': todo_list_id
                  })

@require_http_methods(['POST'])
@decorators.auth_required
@decorators.log_method
def create_task(request: WSGIRequest) -> ty.Any:
    """Adds a new Task to the specified ToDo List"""
    try:
        validator.check_required_params(
            params=request.POST, required=['ToDoListID', 'TaskValue']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.TASKS_PAGE, context={'err': str(err)})

    todo_list_id = request.POST.get('ToDoListID')
    task_val = request.POST.get('TaskValue')

    db_op.create_new_task(todo_list_id, task_val)

    return redirect(config.TASKS_REDIRECT_URL+'/'+todo_list_id)

@require_http_methods(['POST'])
@decorators.auth_required
@decorators.log_method
def update_task(request: WSGIRequest) -> ty.Any:
    """Updates the selected Task in the ToDo List"""
    try:
        validator.check_required_params(
            params=request.POST, required=['NewTaskValue', 'ToDoListID', 'TaskID']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.TODO_LISTS_PAGE, context={'err': str(err)})

    new_task_val = request.POST.get('NewTaskValue')
    todo_list_id = request.POST.get('ToDoListID')
    task_id = request.POST.get('TaskID')
    db_op.update_task_value(todo_list_id, task_id, new_task_val)
    return redirect(config.TASKS_REDIRECT_URL+'/'+todo_list_id)

@require_http_methods(['POST'])
@decorators.auth_required
@decorators.log_method
def delete_task(request: WSGIRequest) -> ty.Any:
    """Deletes the selected Task from the ToDo List"""
    try:
        validator.check_required_params(
            params=request.POST, required=['ToDoListID', 'TaskID']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.TODO_LISTS_PAGE, context={'err': str(err)})

    todo_list_id = request.POST.get('ToDoListID')
    task_id = request.POST.get('TaskID')
    db_op.delete_task_object(todo_list_id, task_id)
    return redirect(config.TASKS_REDIRECT_URL+'/'+todo_list_id)

@require_http_methods(['POST'])
@decorators.auth_required
@decorators.log_method
def toggle_task_status(request: WSGIRequest) -> ty.Any:
    """Toggles the value of `completed` field of the selected Task in
    the ToDo List"""
    try:
        validator.check_required_params(
            params=request.POST, required=['ToDoListID', 'TaskID']
        )
    except ce.InvalidRequestParamsError as err:
        logger.log.error('Error: %s', str(err))
        return render(request, config.TODO_LISTS_PAGE, context={'err': str(err)})

    todo_list_id = request.POST.get('ToDoListID')
    task_id = request.POST.get('TaskID')
    db_op.toggle_completed_value(todo_list_id, task_id)
    return redirect(config.TASKS_REDIRECT_URL+'/'+todo_list_id)
