# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from global_constants.db_enums import MemberRole

# Create your models here.


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class Member(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    email = models.CharField(max_length=30, null=False, blank=False)
    role = models.CharField(max_length=30, choices=MemberRole.choices(), default=MemberRole.REGULAR.value)
    is_active = models.BooleanField(default=True)
    objects = ActiveManager()

    def __unicode__(self):
        return "MemberId: {}, First Name: {}, Last Name: {}, Phone Number: {}, Email: {}, is_active: {} ".format(
               self.id, self.first_name, self.last_name, self.phone_number, self.email, self.role, self.is_active)