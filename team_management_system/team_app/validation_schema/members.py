from django.apps import apps
from global_constants.db_enums import MemberRole


class MembersValidationSchema:
    @staticmethod
    def get_member():
        schema = {
            'id': {
                'type': int,
                'required': False,
                'model_object': apps.get_model(app_label='team_app', model_name='Member'),
                'db_field_reference': 'id',
            }
        }
        return schema

    @staticmethod
    def create_member():
        schema = {
            'first_name': {
                'type': str,
                'required': True,
            },
            'last_name': {
                'type': str,
                'required': True,
            },
            'phone_number': {
                'type': str,
                'required': True,
                'max_length': 10
            },
            'email': {
                'type': str,
                'required': True,
                'model_object': apps.get_model(app_label='team_app', model_name='Member'),
                'unique': True,
                'unique_db_field': 'email',
            },
            'role': {
                'type': str,
                'required': True,
                'allowed': MemberRole.list_choices()
            }
        }
        return schema

    @staticmethod
    def filter_member():
        return MembersValidationSchema.update_filter_common_schema()

    @staticmethod
    def update_member():
        schema = dict()
        schema.update(MembersValidationSchema.get_member())
        schema.update(MembersValidationSchema.update_filter_common_schema())
        return schema

    @staticmethod
    def update_filter_common_schema():
        schema = {
            'first_name': {
                'type': str,
                'required': False,
            },
            'last_name': {
                'type': str,
                'required': False,
            },
            'phone_number': {
                'type': str,
                'required': False,
                'max_length': 10
            },
            'email': {
                'type': str,
                'required': False,
            },
            'role': {
                'type': str,
                'required': False,
                'allowed': MemberRole.list_choices()
            }
        }
        return schema