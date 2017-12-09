from django_logging import log, ErrorLogObject
from datetime import datetime

from team_app.validation_schema.members import MembersValidationSchema
from team_app.error_messages.members import MemberErrors
from global_utils.string_utils import StringUtils
from global_utils.exception_utils import ExceptionUtils
from global_constants import http_constants

from team_app.services.members import MemberService
from team_app.serializers.members import MemberSerializer


def _validate_update_team_member(request_response_obj, **kwargs):
    # Check if there is any parameter for updation
    if not request_response_obj.request_body:
        return False, MemberErrors.NO_UPDATE_PARAMS.value

    member_id = kwargs.get('member_id')
    if not member_id:
        return False, MemberErrors.MISSING_MEMBER_ID.value
    request_response_obj.request_body['id'] = int(kwargs.get('member_id'))
    # Check if request schema is correct
    validation_status, validation_message = request_response_obj.validate_request(
        validation_schema=MembersValidationSchema.update_member())
    if not validation_status:
        return validation_status, validation_message

    # Validate email
    validation_status = StringUtils.correct_email_check(request_response_obj.request_body.get('email'))
    if not validation_status:
        validation_message = MemberErrors.INVALID_EMAIL.value
        return validation_status, validation_message
    # Validate phone number
    validation_status = StringUtils.correct_phone_number_check(request_response_obj.request_body.get('phone_number'))
    if not validation_status:
        validation_message = MemberErrors.INVALID_PHONE.value
    return validation_status, validation_message


def update_team_member(request_response_obj, *args, **kwargs):
    '''
    Update member data
    :param request_response_obj:
    :param args:
    :param kwargs:
    :return:
    '''
    # Validate Request Object
    validation_status, validation_message = _validate_update_team_member(request_response_obj, **kwargs)
    if not validation_status:
        request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.BAD_REQUEST.value
        request_response_obj.response['message'] = validation_message
        return request_response_obj.create_response()

    # Update data for member object
    member_service = MemberService()
    try:
        member_id = request_response_obj.request_body.pop('id', None)
        new_member = member_service.update(filter_params={'id': member_id},
                                           update_params=request_response_obj.request_body)
    except Exception as ex:
        error_message = ExceptionUtils.get_error_message(ex)
        log.error(ErrorLogObject(request_response_obj.request, ex, datetime.now().isoformat()))
        request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.INTERNAL_SERVER_ERROR.value
        request_response_obj.response['message'] = error_message
        return request_response_obj.create_response()

    # Serialize response
    request_response_obj.response['result'] = MemberSerializer.serialize(new_member)
    request_response_obj.http_response_status_code = http_constants.HTTPStatusCode.OK.value
    return request_response_obj.create_response()