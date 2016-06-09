"""eHoshin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import notifications
from django.conf import settings

# If there is a personalized authentication app, this url will use it
# when an /accounts* link is used
urlpatterns = []
if settings.AUTHENTICATION_APP:
    urlpatterns.append(url(r'^accounts', include(settings.AUTHENTICATION_APP + '.urls')))

# Otherwise it's a basic redirection
urlpatterns += [
    url(r'^admin/',                 admin.site.urls),
    url('^\w+/api/notifications/',  include(notifications.urls)),
    url(r'',                        include('users.urls')),
    url(r'',                        include('teams.urls')),
    url(r'',                        include('hoshins.urls'))
]
