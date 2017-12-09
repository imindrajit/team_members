"""team_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from team_app.apis import members_api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/team/', include([
        url(r'^members$', members_api.handle_many_members, name='get_team_members'),
        url(r'^member/(?P<member_id>\d+)/$', members_api.handle_single_member, name='get_each_member'),
        url(r'^member$', members_api.handle_single_member, name='add_update_each_member'),
    ]))
]
