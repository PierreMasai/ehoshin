from django.conf.urls import include, url
from . import views, rest_views

from django.conf import settings

url_users = [
    url(r'^/?$',            rest_views.UserList.as_view()),
    url(r'(?P<pk>[0-9]+)$', rest_views.UserDetail.as_view()),
]

url_accounts = [
    url(r'login',          views.login),
    url(r'logout',         views.logout),
    url(r'signup',         views.signup),

]

url_memberships = [
    url(r'^/?$',            rest_views.MembershipList.as_view()),
    url(r'(?P<pk>[0-9]+)$', rest_views.MembershipDetail.as_view()),
]


urlpatterns = [
    url(r'^users',                              include(url_users)),
    url(r'accounts/me',                         views.user_view),
    url(r'^(?P<team>\w+)/api/memberships', include(url_memberships))
]

if not settings.AUTHENTICATION_APP:
    urlpatterns.append(url(r'^accounts', include(url_accounts)))
