from django_logging import log, ErrorLogObject
from datetime import datetime

from team_app.validation_schema.members import MembersValidationSchema
from global_utils.exception_utils import ExceptionUtils
from global_constants import http_constants

from team_app.services.members import MemberService
from team_app.serializers.members import MemberSerializer


def _validate_get_team_members_with_filters(request_response_obj):
    # Check if request schema is correct
    validation_status, validation_message = request_response_obj.validate_request(
        validation_schema=MembersValidationSchema.update_member())
    return validation_status, validation_message


def get_team_members_with_filters(request_response_obj, *args, **kwargs):
    '''
    Filter team members according to query
    :param request_response_obj:
    :param args:
    :param kwargs:
    :return:
    '''
    # Validate Request Object
    validation_status, validation_message = _validate_get_team_members_with_filters(request_response_obj)
    if not validation_status:
        request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.BAD_REQUEST.value
        request_response_obj.response['message'] = validation_message
        return request_response_obj.create_response()

    # Filters Objects
    member_service = MemberService()
    try:
        members = member_service.get(params=request_response_obj.request_body)
    except Exception as ex:
        error_message = ExceptionUtils.get_error_message(ex)
        log.error(ErrorLogObject(request_response_obj.request, ex, datetime.now().isoformat()))
        request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.INTERNAL_SERVER_ERROR.value
        request_response_obj.response['message'] = error_message
        return request_response_obj.create_response()

    # Serialize response
    request_response_obj.response['result'] = MemberSerializer.serialize(members)
    request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.OK.value
    return request_response_obj.create_response()