from django.test import TestCase
from team_app.tests.factory.member_factory import MemberFactory


class TestMemberUpdate(TestCase):
    def setUp(self):
        self.member_object = MemberFactory.create(first_name="Jim", last_name="Morrison",
                                                  email="jim.morrision@gmail.com", phone_number="9876543210")
        self.success_request_object = {
            'email': "jim.morrison25@gmail.com",
            'phone_number': "7890123456",
            'role': "regular"
        }

        self.failure_request_object = {
            'phone_number': "9876543215",
            'role': "non-admin"
        }

    def test_update_member_success(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.put('/api/v1/team/member/{}/'.format(self.member_object.id),
                                   data=self.success_request_object, content_type='application/json')
        response_json = response.json()
        # Check Status Code
        self.assertEqual(response.status_code, 200)
        # Response Result
        response_result = response_json.get('result')[0]
        # Check First Name
        self.assertEqual(response_result.get('first_name'), self.member_object.first_name)
        # Check Last Name
        self.assertEqual(response_result.get('last_name'), self.member_object.last_name)
        # Check Phone Number
        self.assertEqual(response_result.get('phone_number'), self.success_request_object["phone_number"])
        # Check Email
        self.assertEqual(response_result.get('email'), self.success_request_object["email"])
        # Check Role
        self.assertEqual(response_result.get('role'), self.success_request_object["role"])

    def test_update_member_failure(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.put('/api/v1/team/member/{}/'.format(self.member_object.id),
                                   data=self.failure_request_object, content_type='application/json')
        # Check Status Code
        self.assertEqual(response.status_code, 400)
