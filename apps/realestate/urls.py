# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve

# Could add these to nginx conf too

urlpatterns = [
    #url (r'^img/(?P<path>.*)$',     serve, {'document_root': settings.STATIC_ROOT + '/img',   'show_indexes': True }),
    #url (r'^static2/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True }),
    #url (r'^unify/(?P<path>.*)$',   serve, {'document_root': settings.STATIC_ROOT + '/unify', 'show_indexes': True }),
    url (r'^onepage-assets/(?P<path>.*)$',   serve, {'document_root': settings.STATIC_ROOT + '/onepage-assets', 'show_indexes': True }),
    url (r'^realestate-assets/(?P<path>.*)$',   serve, {'document_root': settings.STATIC_ROOT + '/realestate-assets', 'show_indexes': True }),
    # slider aka _promo, prefixed by theme
    #url (r'^slider/(?P<path>.*)$',    serve, {'document_root': settings.STATIC_ROOT + '/slider',   'show_indexes': True }),
    url (r'^realestate/(?P<path>.*)$',    serve, {'document_root': settings.STATIC_ROOT + '/realestate',   'show_indexes': True }),
  ]
