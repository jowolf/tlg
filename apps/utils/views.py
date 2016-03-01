import functools, re

#from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admindocs.views import simplify_regex
#from django.conf import settings
from django_extensions.management.commands.show_urls import Command

from tlg.urls import urlpatterns
from .minitags import table, tr, td, th, html, a

'''no
#[h,kl]uge
from django.core.management import color
import django_extensions.management.color as decolor
#from decolor import _dummy_style_func

def noop_color_style():
  style = color.color_style()
  for role in ('INFO', 'WARN', 'BOLD', 'URL', 'MODULE', 'MODULE_NAME', 'URL_NAME'):
    setattr(style, role, lambda msg: msg)
  return style

decolor.color_style = noop_color_style
'''

@login_required
def show_urls (request, app):  # app NYI
  #urls = Command(no_color=True).handle (app, format_style='dense', urlconf='ROOT_URLCONF')  # settings.ROOT_URLCONF)

  view_funcs = Command (no_color=True).extract_views_from_urlpatterns (urlpatterns)
  views = []
  decorator = ['login_required']

  for (func, regex, url_name) in view_funcs:
    if hasattr(func, '__globals__'):
      func_globals = func.__globals__
    elif hasattr(func, 'func_globals'):
      func_globals = func.func_globals
    else:
      func_globals = {}

    decorators = [d for d in decorator if d in func_globals]

    if isinstance (func, functools.partial):
      func = func.func
      decorators.insert (0, 'functools.partial')

    if hasattr(func, '__name__'):
      func_name = func.__name__
    elif hasattr(func, '__class__'):
      func_name = '%s()' % func.__class__.__name__
    else:
      func_name = re.sub(r' at 0x[0-9a-f]+', '', repr(func))

    module='{0}.{1}'.format (func.__module__, func_name)
    url = simplify_regex(regex)

    # should be able to sort by and /or place each column first
    views += [(url, module, url_name or '', ', '.join(decorators))]
    # text - old - could do by parm
    #views += [', '.join ((url, module, url_name or '', ', '.join(decorators)))]

  content = table (
      th (['url','model','name','decorator(s)']) +
      tr ([td (a(line[0],href=line[0])) + td (line[1:]) for line in views])
    )
  #urls = '\n'.join (views)

  page = html (content)
  return HttpResponse (page)

  #return render (request, 'base.html', dict (content = content))
  #return HttpResponse (urls, content_type="text/plain")  # "application/xhtml+xml")

