import factory
from team_app.models import Member
import random
from global_constants.db_enums import MemberRole


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    '''LazyAttribute creates email after the object is created'''
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    phone_number = factory.Faker('phone_number')
    role = random.choice(MemberRole.list_choices())
