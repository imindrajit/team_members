from django.test import TestCase


class TestMemberCreate(TestCase):
    def setUp(self):
        self.success_request_object = {
            "first_name": "Jim",
            "last_name": "Morrison",
            "email": "jim.morrison@gmail.com",
            "phone_number": "9876543210",
            "role": "admin"
        }

        self.failure_request_object = {
            'first_name': "Jim",
            'last_name': "Morrison",
            'email': "jim.morrison",
            'phone_number': "987654321",
            'role': "admin"
        }

    def test_create_member_success(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.post('/api/v1/team/member', data=self.success_request_object,
                                    content_type='application/json')
        response_json = response.json()
        # Check Status Code
        self.assertEqual(response.status_code, 200)
        # Response Result
        response_result = response_json.get('result')[0]
        # Check First Name
        self.assertEqual(response_result.get('first_name'), self.success_request_object["first_name"])
        # Check Last Name
        self.assertEqual(response_result.get('last_name'), self.success_request_object["last_name"])
        # Check Phone Number
        self.assertEqual(response_result.get('phone_number'), self.success_request_object["phone_number"])
        # Check Email
        self.assertEqual(response_result.get('email'), self.success_request_object["email"])
        # Check Role
        self.assertEqual(response_result.get('role'), self.success_request_object["role"])

    def test_create_member_failure(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.post('/api/v1/team/member', data=self.failure_request_object,
                                    content_type='application/json')
        # Check Status Code
        self.assertEqual(response.status_code, 400)
