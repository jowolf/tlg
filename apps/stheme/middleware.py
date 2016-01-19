# -*- coding: utf-8 -*-

#import threading
from threading import current_thread

#_local = threading.local()

#from django.conf import settings
#from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect

#class ThemePathMiddleware(object):
#    """
#    Handles static & template paths for different themes
#    """
#    def process_request(self, request):
#        print settings.STATIC_ROOT
#        print settings.TEMPLATE_DIRS
#
#        if request.get_full_path().endswith ('?theme=tshop'):
#            settings.STATIC_ROOT += '/tshop'
#            #settings.TEMPLATE_DIRS [0] += '/tshop' "tuple does not support item assignment"
#            settings.TEMPLATE_DIRS = [p for p in settings.TEMPLATE_DIRS]
#            settings.TEMPLATE_DIRS [0] += '/tshop'

class ThemeLocalRequestMiddleware (object):
    def process_request(self, request):
        # NFG, doesnt even work:
        #mythread = threading.local()
        #mythread.request = request
        #print 'in Middleware:',  mythread.__dict__.keys(), threading.active_count(), threading.current_thread(), threading.current_thread().__dict__
        #
        # but this does:
        #threading.current_thread().__dict__ ['request2'] = 'blah'
        current_thread().__dict__ ['request'] = request