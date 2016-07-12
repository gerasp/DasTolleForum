"""TollesForum URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views
import forum.views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', forum.views.index, name='welcome'),
    url(r'^welcome$', forum.views.index, name='welcome'),

    url(r'^topics$', forum.views.show_topics),
    url(r'^topics/add$', forum.views.add_or_edit_topic),
    url(r'^topics/edit/(?P<pk>[0-9]+)$', forum.views.add_or_edit_topic),
    url(r'^topics/remove/(?P<pk>[0-9]+)$', forum.views.remove_topic),

    url(r'^(?P<pk>[0-9]+)/threads$', forum.views.show_threads),
    url(r'^(?P<pk>[0-9]+)/threads/add$', forum.views.add_or_edit_thread),
    url(r'^(?P<pk>[0-9]+)/threads/edit/(?P<pk2>[0-9]+)$', forum.views.add_or_edit_thread),
    url(r'^(?P<pk>[0-9]+)/threads/remove/(?P<pk2>[0-9]+)$', forum.views.remove_thread),

    url(r'^(?P<pk>[0-9]+)/(?P<pk2>[0-9]+)/messages$', forum.views.show_messages),

    url(r'^search', forum.views.search),

    url(r'^accounts/signup$', forum.views.signup),
    url(r'^accounts/login/$', django.contrib.auth.views.login),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, {'next_page': '/welcome'}),
    url(r'^accounts/change_avatar/$', forum.views.change_avatar),

    url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT,  }),
]
