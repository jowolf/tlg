# -*- coding: utf-8 -*-

#import threading
from threading import current_thread

class ThemeLocalRequestMiddleware (object):
    def process_request(self, request):
        current_thread().__dict__ ['request'] = request
