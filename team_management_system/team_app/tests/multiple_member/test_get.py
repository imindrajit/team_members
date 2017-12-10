from django.test import TestCase
from team_app.tests.factory.member_factory import MemberFactory
from global_constants.db_enums import MemberRole


class TestMemberGetWithFilters(TestCase):
    def setUp(self):
        self.member_object = MemberFactory.create(first_name="Jim", last_name="Morrison",
                                                  email="jim.morrision@gmail.com", phone_number="9876543210")
        self.member_object2 = MemberFactory.create(first_name="Bill", last_name="Gates",
                                                  email="bill.gates@gmail.com", phone_number="8976452310")

    def test_get_member_with_filters_success(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.get('/api/v1/team/members', content_type='application/json')
        response_json = response.json()
        # Check Status Code
        self.assertEqual(response.status_code, 200)
        # Response Result
        response_result = response_json.get('result')
        # Length of result
        self.assertEqual(len(response_result), 2)
        # Check First Name
        self.assertEqual(response_result[0].get('first_name'), self.member_object.first_name)
        # Check Last Name
        self.assertEqual(response_result[0].get('last_name'), self.member_object.last_name)
        # Check Phone Number
        self.assertEqual(response_result[0].get('phone_number'), self.member_object.phone_number)
        # Check Email
        self.assertEqual(response_result[0].get('email'), self.member_object.email)
        # Check Role
        self.assertTrue(response_result[0].get('role') in MemberRole.list_choices())

        # Check First Name
        self.assertEqual(response_result[1].get('first_name'), self.member_object2.first_name)
        # Check Last Name
        self.assertEqual(response_result[1].get('last_name'), self.member_object2.last_name)
        # Check Phone Number
        self.assertEqual(response_result[1].get('phone_number'), self.member_object2.phone_number)
        # Check Email
        self.assertEqual(response_result[1].get('email'), self.member_object2.email)
        # Check Role
        self.assertTrue(response_result[1].get('role') in MemberRole.list_choices())

    def test_get_member_with_filters_failure(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.get('/api/v1/team/members?new_name=random', content_type='application/json')
        # Check Status Code
        self.assertEqual(response.status_code, 400)
