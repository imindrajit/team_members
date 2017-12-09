from django.test import TestCase
from team_app.tests.factory.member_factory import MemberFactory


class TestMemberDelete(TestCase):
    def setUp(self):
        self.member_object = MemberFactory.create(first_name="Jim", last_name="Morrison",
                                                  email="jim.morrision@gmail.com", phone_number="9876543210")

    def test_delete_member_success(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.delete('/api/v1/team/member/{}/'.format(self.member_object.id),
                                    content_type='application/json')
        response_json = response.json()
        # Check Status Code
        self.assertEqual(response.status_code, 200)
        # Check Response Result
        self.assertEqual(response_json.get('result'), {})
        # Check Response Message
        self.assertEqual(response_json.get('message'), str())

    def test_delete_member_failure(self):
        '''
        Call API directly using client in django tests
        :return:
        '''
        response = self.client.delete('/api/v1/team/member/{}/'.format(self.member_object.id + 10),
                                    content_type='application/json')
        # Check Status Code
        self.assertEqual(response.status_code, 400)
