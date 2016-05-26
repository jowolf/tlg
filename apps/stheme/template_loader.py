# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache

#from django.template.loaders.app_directories import app_template_dirs, Loader as AppDirLoader
from django.template.loaders.app_directories import Loader as AppDirLoader
from django.utils._os import safe_join

#import threading
from threading import current_thread

themes = settings.THEMES
default_theme = settings.DEFAULT_THEME
#current_theme = default_theme

trace = 0

my_app_path = safe_join (os.path.dirname (__file__), 'templates')

class Loader (AppDirLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Adds the theme to the end of this (the 'stheme') app's path, if theme cookie or request is present.
        Saves theme in session if so.
        normalizes for / in path, etc.
        """

        global default_theme #, current_theme

        req = current_thread().__dict__.get ('request', None)

        if not req: print 'REQUEST IS NULL'

        if trace: print req is not None, template_name

        if req and hasattr (req, 'session'):
            ses = req.session
            theme = req.GET.get ('theme') or ses.get ('theme', None)

            if theme and '?theme=' in theme:  # work around Django bug & Baidu spider passing "?theme=tshop?theme=tshop" which comes through as list
              theme = theme.rsplit ('=', 1)[-1]

            if not theme:
              theme = default_theme

            if theme:
              theme = theme.strip('/')
              ses ['theme'] = theme
              #if theme != current_theme:
              #  messages.success (req, 'Theme switched to: %s' % theme)
              #  try:
              #    cache.clear()
              #  except Exception, e:
              #    print 'Why:', e, 'cache', cache
              #  messages.info (req, 'Cache cleared')
              #  current_theme = theme

            if trace: print theme

            try:
              if theme:
                #yield safe_join(my_app_path, theme, template_name)  # avoid 'SuspiciousFileOperation'
                # 4/23/16 JJW address directory trav vuln:
                pth = os.path.normpath (os.path.join(my_app_path, theme, template_name))
                if not pth.startswith (my_app_path):
                  pth = os.path.join(my_app_path, default_theme, template_name)
                yield pth  # os.path.join(my_app_path, theme, template_name)
              else:
                #yield safe_join(my_app_path, template_name)  # ditto
                yield os.path.join(my_app_path, template_name)
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't valid UTF-8. return default theme.
                yield os.path.join(my_app_path, default_theme, template_name)
            except ValueError:
                # The joined path was located outside of template_dir.
                pass

