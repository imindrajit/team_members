from team_app.models import Member


class MemberService:
    def create(self, params={}):
        '''
        Create Member object using key value pairs in kwargs
        :param args:
        :param kwargs:
        :return:
        '''
        return Member.objects.create(**params)

    def get(self, params={}):
        '''
        Return all members matching the filter query
        :param args:
        :param kwargs:
        :return:
        '''
        return Member.objects.filter(**params)

    def delete(self, params={}):
        '''
        Soft Delete matching member. Set is_active = False
        :param params:
        :return:
        '''
        member = self.get(params=params)
        member.update(is_active=False)
        return member

    def update(self, filter_params={}, update_params={}):
        '''
        Update Member object with new set of values
        :param params:
        :return:
        '''
        members = self.get(params=filter_params)
        members.update(**update_params)
        return members