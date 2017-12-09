from django.views.decorators.csrf import csrf_exempt
from django_logging import log, ErrorLogObject
from datetime import datetime

from global_utils.request_response_utils import RequestResponseUtils
from global_utils.exception_utils import ExceptionUtils
from global_constants import http_constants

from team_app.apis.single_member.add import add_new_team_member
from team_app.apis.single_member.get import get_team_member
from team_app.apis.single_member.delete import delete_team_member
from team_app.apis.single_member.update import update_team_member
from team_app.apis.multiple_member.get import get_team_members_with_filters


@csrf_exempt
def handle_single_member(request, *args, **kwargs):
    '''
    Execute operations on a single member entity based on request http method
    :param request: http request
    :param args:
    :param kwargs:
    :return: http response
    '''
    http_response = None
    request_response_obj = RequestResponseUtils(request=request)
    try:
        if request_response_obj.http_request_method == http_constants.HTTPMethod.POST.value:
            # Create a new member
            http_response = add_new_team_member(request_response_obj, *args, **kwargs)
        elif request_response_obj.http_request_method == http_constants.HTTPMethod.PUT.value:
            # Update a member
            http_response = update_team_member(request_response_obj, *args, **kwargs)
        elif request_response_obj.http_request_method == http_constants.HTTPMethod.GET.value:
            # Get a member
            http_response = get_team_member(request_response_obj, *args, **kwargs)
        elif request_response_obj.http_request_method == http_constants.HTTPMethod.DELETE.value:
            # Delete a member
            http_response = delete_team_member(request_response_obj, *args, **kwargs)
        return http_response
    except Exception as ex:
        error_message = ExceptionUtils.get_error_message(ex)
        log.error(ErrorLogObject(request, ex, datetime.now().isoformat()))
        request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.INTERNAL_SERVER_ERROR.value
        request_response_obj.response['message'] = error_message
        return request_response_obj.create_response()


@csrf_exempt
def handle_many_members(request, *args, **kwargs):
    '''
    Execute operations on a multiple member entities based on request http method
    :param request: http request
    :param args:
    :param kwargs:
    :return: http response
    '''
    request_response_obj = RequestResponseUtils(request=request)
    if request_response_obj.http_request_method == http_constants.HTTPMethod.GET.value:
        # GET team members, either all or using filters
        try:
            http_response = get_team_members_with_filters(request_response_obj, *args, **kwargs)
            return http_response
        except Exception as ex:
            error_message = ExceptionUtils.get_error_message(ex)
            log.error(ErrorLogObject(request, ex, datetime.now().isoformat()))
            request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.INTERNAL_SERVER_ERROR.value
            request_response_obj.response['message'] = error_message
            return request_response_obj.create_response()