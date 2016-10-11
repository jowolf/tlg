# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from apps.utils.views import show_urls


urlpatterns = [
    url (r'^show_urls/(?P<app>.*)$', show_urls,),
  ]
