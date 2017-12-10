from django.shortcuts import HttpResponse
import json
import ast
from enum import Enum

from global_constants import http_constants
from global_utils.string_utils import StringUtils


class RequestResponseUtils(object):
    def __init__(self, request=None):
        self.request = request
        self.request_body = self._parse_request_body()
        self.response = {
            'result': {},
            'message': str(),
        }
        self.http_request_method = self._get_request_method()
        self.http_response_status_code = None

    def _get_request_method(self):
        '''
        Get the HTTP Request Method
        :return:
        '''
        if self.request.method == http_constants.HTTPMethod.POST.value:
            return http_constants.HTTPMethod.POST.value
        elif self.request.method == http_constants.HTTPMethod.GET.value:
            return http_constants.HTTPMethod.GET.value
        elif self.request.method == http_constants.HTTPMethod.PUT.value:
            return http_constants.HTTPMethod.PUT.value
        elif self.request.method == http_constants.HTTPMethod.DELETE.value:
            return http_constants.HTTPMethod.DELETE.value
        return None

    def _parse_request_body(self):
        '''
        :return: request data in json format
        '''
        parsed_data = {}
        try:
            if self.request.method in [http_constants.HTTPMethod.POST.value, http_constants.HTTPMethod.PUT.value]:
                parsed_data = ast.literal_eval(self.request.body)
            elif self.request.method in [http_constants.HTTPMethod.GET.value, http_constants.HTTPMethod.DELETE.value]:
                parsed_data = dict()
                for key, val in self.request.GET.iterlists():
                    if len(val) > 1:
                        parsed_data[key] = val
                    else:
                        try:
                            parsed_data[key] = eval(val[0])
                        except:
                            parsed_data[key] = val[0]
        except:
            parsed_data = {}
        return parsed_data

    def validate_request(self, validation_schema):
        '''
        Validate Request Body against a validation schema
        :param validation_schema:
        :return:
        '''
        validator = Validator(request_body=self.request_body, validation_schema=validation_schema)
        valid_status, message = validator.validate_request_object()
        return valid_status, StringUtils.convert_list_to_string(message)

    def create_response(self):
        '''
        :param message: message for the API request. Empty in case of success.
        :param result: json output of the API calls
        :param http_status_code: Standard HTTP STATUS Code
        :return: response object
        '''
        response = {
            'result': self.response.get('result')
        }
        message = self.response.get('message')
        if isinstance(message, dict):
            message = StringUtils.convert_error_json_to_string(message)
        response['message'] = message
        return HttpResponse(json.dumps(response), content_type='application/json',
                                       status=self.http_response_status_code)


class ErrorMessages(Enum):
    PARAMS = 'Allowed request params - {}. Params in sent request - {}.'
    TYPE = '{} should be of type {}.'
    REQUIRED = '{} is a mandatory field.'
    ALLOWED = '{} does not have a valid value.'
    SCHEMA_TYPE = 'Contents of {} should be of type {}.'
    MAX_LENGTH = 'Max length for {} can be {}.'
    MODEL_OBJECT = 'Invalid {}.'
    RANGE = 'Allowed values for {} are in between {} and {}.'
    UNIQUE = '{} field is unique. {} already exists.'


class Schema(object):
    def __init__(self, key, schema_dict):
        self.field = key
        self.type = None
        self.required = None
        self.unique = None
        self.unique_db_field = None
        self.schema_type = None
        self.allowed = None
        self.max_length = None
        self.model_object = None
        self.db_field_reference = None
        self.range = None

        for key, value in schema_dict.items():
            setattr(self, key, value)

    def _validate_required(self, value):
        if self.required and (value or value == 0):
            return True
        elif self.required and not value:
            return False
        return True

    def _validate_max_length(self, value):
        valid = True
        if not self.required and not value:
            return valid
        else:
            if self.type == str:
                if len(value) > self.max_length:
                    valid = False
        return valid

    def _validate_type(self, value):
        if not self.required and not value:
            return True
        if value and isinstance(self.type, list):
            return type(value) in self.type
        elif value:
            return type(value) == self.type
        return True

    def _validate_allowed(self, value):
        if not self.required and not value:
            return True
        if not isinstance(value, list):
            return value in self.allowed
        else:
            return all(val in self.allowed for val in value)

    def _validate_range(self, value):
        if not self.required and not value:
            return True
        if value and self.range[0] <= value <= self.range[1]:
            return True
        return False

    def _validate_model_object(self, value):
        if not self.required and not value:
            return True
        if value:
            if self.model_object and self.db_field_reference:
                model_obj = self.model_object.objects.filter(**{self.db_field_reference: value})
                if model_obj:
                    return True
                return False
            return False
        return False

    def _validate_unique_field(self, value):
        if not self.required and not value:
            return True
        if value:
            if self.model_object and self.unique and self.unique_db_field:
                model_obj = self.model_object.objects.filter(**{self.unique_db_field: value})
                if not model_obj:
                    return True
                return False
            return False
        return False

    def _validate_schema_type(self, values):
        validation_status = True
        if not self.required and not values:
            return validation_status
        for each_val in values:
            if not isinstance(each_val, self.schema_type):
                validation_status = False
                break
        return validation_status

    def validate_schema(self, val):
        final_validation_status, error_message = True, str()
        if self.required:
            validation_status = self._validate_required(val)
            if not validation_status:
                error_message += ' '
                error_message += ErrorMessages.REQUIRED.value.format(self.field)
                final_validation_status = final_validation_status and validation_status
        if self.type:
            validation_status = self._validate_type(val)
            if not validation_status:
                error_message = ErrorMessages.TYPE.value.format(self.field, self.type)
                final_validation_status = final_validation_status and validation_status
        if self.max_length:
            validation_status = self._validate_max_length(val)
            if not validation_status:
                error_message = ErrorMessages.MAX_LENGTH.value.format(self.field, self.max_length)
                final_validation_status = final_validation_status and validation_status
        if self.allowed:
            validation_status = self._validate_allowed(val)
            if not validation_status:
                error_message += ' '
                error_message += ErrorMessages.ALLOWED.value.format(self.field)
                final_validation_status = final_validation_status and validation_status
        if self.range:
            validation_status = self._validate_range(val)
            if not validation_status:
                error_message += ' '
                error_message += ErrorMessages.RANGE.value.format(self.field, self.range[0], self.range[1])
                final_validation_status = final_validation_status and validation_status
        if self.model_object and self.db_field_reference:
            validation_status = self._validate_model_object(val)
            if not validation_status:
                error_message += ' '
                error_message += ErrorMessages.MODEL_OBJECT.value.format(self.field)
                final_validation_status = final_validation_status and validation_status
        if self.model_object and self.unique and self.unique_db_field:
            validation_status = self._validate_unique_field(val)
            if not validation_status:
                error_message += ' '
                error_message += ErrorMessages.UNIQUE.value.format(self.field, val)
                final_validation_status = final_validation_status and validation_status
        if self.schema_type:
            validation_status = self._validate_schema_type(val)
            if not validation_status:
                error_message += ' '
                error_message += ErrorMessages.SCHEMA_TYPE.value.format(self.field, self.schema_type)
                final_validation_status = final_validation_status and validation_status
        return final_validation_status, error_message


class Validator(object):
    def __init__(self, request_body, validation_schema, allow_extra_request_params=False):
        self.validation_schema = validation_schema
        self.request_body = request_body
        self.error_messages = list()
        self.validation_status = True
        self.allow_extra_request_params = allow_extra_request_params

    def validate_request_object(self):
        if not self.allow_extra_request_params:
            request_params = self.request_body.keys()
            allowed_params = self.validation_schema.keys()
            for each_param in request_params:
                if str(each_param) not in allowed_params:
                    self.validation_status = False
                    break
            if not self.validation_status:
                self.error_messages.append(ErrorMessages.PARAMS.value.format(allowed_params, request_params))
        if self.validation_status:
            for key in self.validation_schema:
                schema = Schema(key, self.validation_schema[key])
                value = str(self.request_body.get(key)) if type(self.request_body.get(key)) == unicode \
                    else self.request_body.get(key)
                if isinstance(value, list):
                    for i in xrange(len(value)):
                        value[i] = str(value[i]) if type(value[i]) == unicode else value[i]
                valid_status, error_message = schema.validate_schema(value)
                self.validation_status = self.validation_status and valid_status
                if not valid_status:
                    self.error_messages.append(error_message)
        return self.validation_status, self.error_messages