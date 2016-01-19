# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.conf import settings
#from django.http import HttpResponse


urlpatterns = patterns('',
    #(r'^test2/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),
    (r'^assan/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/assan', 'show_indexes': True }),
    (r'^tshop/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/tshop', 'show_indexes': True }),
    (r'^unify/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/unify', 'show_indexes': True }),
    #(r'^legacy/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/legacy', 'show_indexes': True }),
)
