from django.test import TestCase
from team_app.tests.factory.member_factory import MemberFactory
from global_constants.db_enums import MemberRole


class TestMemberGet(TestCase):
    def setUp(self):
        self.member_object = MemberFactory.create(first_name="Jim", last_name="Morrison",
                                                  email="jim.morrision@gmail.com", phone_number="9876543210")

    def test_get_member_success(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.get('/api/v1/team/member/{}/'.format(self.member_object.id),
                                    content_type='application/json')
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
        self.assertEqual(response_result.get('phone_number'), self.member_object.phone_number)
        # Check Email
        self.assertEqual(response_result.get('email'), self.member_object.email)
        # Check Role
        self.assertTrue(response_result.get('role') in MemberRole.list_choices())

    def test_get_member_failure(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.get('/api/v1/team/member/{}/'.format(self.member_object.id + 10),
                                    content_type='application/json')
        # Check Status Code
        self.assertEqual(response.status_code, 400)
