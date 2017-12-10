import re


class StringUtils:
    @staticmethod
    def convert_list_to_string(list_values):
        string = ','.join(item for item in list_values if item)
        return string

    @staticmethod
    def convert_error_json_to_string(error_json):
        error_msg = str()
        for key in error_json.keys():
            if error_msg != '':
                error_msg += ', '
            error_msg += '{}'.format(key)
            for val in error_json[key]:
                error_msg += ' {}'.format(val)
        return error_msg

    @staticmethod
    def correct_email_check(email):
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(re.search(EMAIL_REGEX, email))

    @staticmethod
    def correct_phone_number_check(phone_number):
        PHONE_NUMBER_REGEX = re.compile(r"[789]\d{9}?")
        return bool(re.search(PHONE_NUMBER_REGEX, phone_number))
