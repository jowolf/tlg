# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve

# Could add these to nginx conf too (not static2)

urlpatterns = [
    url (r'^img/(?P<path>.*)$',     serve, {'document_root': settings.STATIC_ROOT + '/img',   'show_indexes': True }),
    url (r'^css/(?P<path>.*)$',     serve, {'document_root': settings.STATIC_ROOT + '/css',   'show_indexes': True }),
    url (r'^unify-assets/(?P<path>.*)$',   serve, {'document_root': settings.STATIC_ROOT + '/unify-assets', 'show_indexes': True }),
    #url (r'^static2/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),
  ]
