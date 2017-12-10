from global_utils.choice_enum_utils import ChoiceEnum


class HTTPMethod(ChoiceEnum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"


class HTTPStatusCode(ChoiceEnum):
    OK = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500