from django.conf.urls import include, url
from . import views

url_api = [
    url(r'^/?$',            views.rest_api_list),
    url(r'(?P<pk>[0-9]+)$', views.rest_api_detail),
]

urlpatterns = [
    url(r'^\w+/api/leader_synthesis/(?P<pk>[0-9]+)$',   views.get_leader_synthesis),
    url(r'^\w+/api/hoshin_synthesis/(?P<pk>[0-9]+)$',   views.get_hoshin_synthesis),

    url(r'^(?P<name>\w+)/api/(?P<object_type>\w+)', include(url_api)),
]
