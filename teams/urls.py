from django.conf.urls import include, url
from . import views, rest_views

url_teams = [
    url(r'^/?$',            rest_views.TeamList.as_view()),
    url(r'(?P<pk>[0-9]+)$', rest_views.TeamDetail.as_view()),
]

url_settings = [
    url(r'^/?$',   views.dashboard_settings),
    url(r'basics', views.basic_settings),
    url(r'users',  views.users_settings),
]

urlpatterns = [
    url(r'^/?$',                                    views.home),
    url(r'^teams',                                  include(url_teams)),

    url(r'^(?P<team_name>\w+)/api/references/(?P<ref_name>[^/]+)$', views.get_reference),
    url(r'^(?P<name>\w+)/settings',                 include(url_settings)),
    url(r'^(?P<name>\w+)/?$',                       views.team_home),
    url(r'^(?P<name>\w+)/(\d+)',                       views.team_home),
]
