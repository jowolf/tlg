# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include


urlpatterns = patterns('',
    (r'^show_urls/(?P<app>.*)$', 'apps.utils.views.show_urls',),
)
