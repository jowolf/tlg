# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf import settings
#from django.http import HttpResponse
from django.views.static import serve


urlpatterns = [
    #url (r'^test2/(?P<path>.*)$',  serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),
    #url (r'^assan/(?P<path>.*)$',  serve, {'document_root': settings.STATIC_ROOT + '/assan', 'show_indexes': True }),
    #url (r'^tshop/(?P<path>.*)$',  serve, {'document_root': settings.STATIC_ROOT + '/tshop', 'show_indexes': True }),
    url (r'^img/(?P<path>.*)$',     serve, {'document_root': settings.STATIC_ROOT + '/img',   'show_indexes': True }),
    url (r'^unify/(?P<path>.*)$',   serve, {'document_root': settings.STATIC_ROOT + '/unify', 'show_indexes': True }),
    url (r'^static2/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),
  ]
