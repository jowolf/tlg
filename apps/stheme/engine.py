import pyquery, os, sys, argparse, yaml, html5lib, lxml, re
import cssutils

from pyquery import PyQuery as pq
from pprint import pprint
from utils import ensure_dirs, ensure_local, my_slugify_url, dt, stylus_compile
from jade import jade2django
from string import Template
from html2shpaml import convert as convert_to_shpaml
#from django_stylus.templatetags.stylus import compileit as stylus_compile

# my ordered-dict solution, works, as well as line numbers:
from yaml_ordered import ordered_load_all, lines as yaml_lines
from collections import OrderedDict

try:
    from shpaml.shpaml import convert_text
except:
    from shpaml import convert_text

trace = 1

#config, declarations, transformations = [d for d in ordered_load_all (open(map_file))] [:3]  # >3 are cmnts

config, declarations = {}, {}
templates_path = None

my_path       = os.path.abspath (os.path.dirname (__file__))
theme_path    = my_path + '/themes/'
apps_path     = os.path.dirname (my_path)  # once for 'apps'
project_path  = os.path.dirname (apps_path)  # twice for one-below 'apps'
static_path   = os.path.join (my_path, 'static')

config.update (
  my_path       = my_path,
  theme_path    = theme_path,
  apps_path     = apps_path,
  project_path  = project_path,
  static_path   = static_path,
)

def update_config (kv):
  global config, templates_path

  config.update (kv)
  #if trace: print 'Config keys:', config.keys()

  # could do inject_locals or inject_globals, here
  theme_name            = config ['theme_name']
  theme_url             = config ['theme_url']
  download              = config.get ('download', 0)  # optional
  templates_path        = config ['templates_path']
  theme_downloaded_path = config ['theme_downloaded_path']

  static_link           = os.path.join (static_path, theme_name)
  templates_path        = Template (templates_path).safe_substitute (config)
  theme_downloaded_path = Template (theme_downloaded_path).safe_substitute (config)

  config.update (
    static_link           = static_link,
    templates_path        = templates_path,
    theme_downloaded_path = theme_downloaded_path,
  )

  if trace: print 'Config:', ; pprint (config)

  # This should be moved to a linkstatic management command:
  # Also see the README in the stheme/static dir, and the theme's assets/css dirs
  # these links should be relative, not absolute, see test_relpath.py - or at least don't overwrite them if they are there already
  if not os.path.exists (static_link) and not os.path.islink (static_link):
    os.symlink (theme_downloaded_path, static_link)

  try:
    sys.path.append (project_path)
    sys.path.append (apps_path)
    os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'eracks.settings')
    import django
    django.setup()
    from django.conf import settings as django_settings
    from django.apps import apps as django_apps
    django_app_paths = [p for p in django_apps.get_app_paths()
                        if p.startswith (apps_path) and not p.startswith (my_path)]
    if trace: pprint (django_app_paths)
    django_present = 1
  except:
    django_present = 0

  if download:
    raise Exception ('Deprecated - use cached url instead')


class Operations (object):
  '''
  Operations is mostly a sublass/abc for other file manipulators -
  eg, html(5) parser/serializer - bs4 vs lxml vs html5lib, etc
  also css, generic file, etc - could also use for yaml (or space, coffee) input
  '''
  def __init__ (self, node, value):
    self.root = node  # a root-level node, usually a filename
    self.dct = value  # level-1 or root-level dict
    self.actions = [fn for fn in dir (self)
        if not fn.startswith ('_') and callable (self.__getattribute__ (fn))] # break out into classmethod
    self.map_line = yaml_lines [node] if yaml_lines else 0  # future: pass in yamlops inst which owns lines
    self.context = None
    if trace:
      print 'MAP_LINE:', self.map_line, node
      print 'CLASS:', self.__class__
      print 'ACTIONS:', self.actions

  def apply (self, context, data):
    if trace & 2:
      try:
        print '%s: apply; context: %s; data: %s' % (self.__class__.__name__, context, data)
      except UnicodeEncodeError:
        print 'ANNOYING UNICODE BS AGAIN'
    op = context # for 'apply', this edge case
    if op in self.actions:
      # With getattribute, the method is bound already, no need to pass in self
      self.__getattribute__ (op) (self.context, data)
    else:
      if isinstance (data, (list, tuple)):
        for item in data:
          self.unknown (op, item)
      else:
        self.unknown (op, data)

  def unknown (self, op, data):
    raise Exception ('Unknown Action / Operation - Base Class')

  def comment (self, *args):
    if trace: print 'COMMENT:', args
    pass

  def finalize (self):  # , a, b):
    raise Exception ('NYI - Base Class')

  def __call__ (self):  # main loop
    for k,v in self.dct.items():
      if trace:
        print
        print 'IN BASE CALL: k:%s v:%.50s' % (k,v)
      self.apply (k, v)  # (op, data)

    self.finalize()

  def read (self, context, fname=None):
    if fname is None:
      fname = self.fname

    fname = Template (fname).safe_substitute (config)

    with open (fname) as f:
      self.content = f.read()
      if trace: print fname, 'READ OK'

  def write (self, context, fname):
    if fname is None:
      fname = self.fname

    fname = Template (fname).safe_substitute (config)

    if fname.startswith ('/'):  # assume the caller know what they are doing, and it's a full path
      pth = fname
    else:
      ensure_dirs (templates_path + fname)
      pth = templates_path + fname

    content = context or self.content

    with open (pth, 'w') as f:
      f.write (content.encode ('UTF-8'))
      if trace: print fname, 'WRITE OK'


class YamlOperation (Operations):
  '''
  YamlOperation just reads a yaml file and includes in declarations - value to the right of the colon is a comment
  This could be a superclass of Operations, actually, with just init and maybe read..
  ToDo: integrate YAML line numbering, config updates, perhaps manage global state
  '''
  def __call__ (self):
    global map_file  # TODO: objectify the Yaml file and line number handling into this class, and away from globals
    map_file = self.root

    self.root = Template (self.root).safe_substitute (config)

    yaml_docs = [d for d in ordered_load_all (open (self.root))]

    for yaml_doc in yaml_docs:
      if yaml_doc and not 'ignore' in yaml_doc:
        for k,v in yaml_doc.items():
          if trace: print 'key:', k
          if k == "config":
            update_config (v)
          else:
            ops = construct_operations (k,v)
            if ops:
              ops()
            else:
              declarations.update ([(k,v)])



class FileOperations (Operations):  # CssOperations should be css-aware, and wrap cssutils
  notice = '''\

/*  WARNING: GENERATED FILE - EDITS WILL BE LOST  */
/*  GENERATED FROM: %s at line %s on %s   */

'''
  def replace (self, context, data):
    for k,v in data.items():
      self.content = self.content.replace (k,v)

  def ireplace (self, dummy, data):
    for k,v in data.items():
      self.content = re.sub ('(?i)' + re.escape (k), v, self.content)

  def symlink (self, dummy, dest_fname):
    dest_fname = Template (dest_fname).safe_substitute (config)
    if trace: print 'SYMLINK:', templates_path + self.root, dest_fname
    # Don't blow away exisitng one if there - may have been done by hand due to need to be relative
    #if os.path.islink (dest_fname):
    #  os.unlink (dest_fname)
    # Should be option for relative symlink, anyway, or by default! see test_relpath.py
    if not os.path.exists (dest_fname) and not os.path.islink (dest_fname):
      os.symlink (templates_path + self.root, dest_fname)

  def finalize (self):
    fname = self.root
    self.content = self.notice % (map_file, self.map_line, dt()) + self.content
    self.write (None, fname)


class CssOperations (FileOperations):  # CssOperations should be css-aware, and wrap cssutils
  def show_urls (s, data):
    stylesheet = cssutils.parseString (s)  # parseFile (f)  # its a start :)
    #print [u for u in cssutils.getUrls (stylesheet)]
    for u in cssutils.getUrls (stylesheet):
      print u


# class MinamlCompileOperation (Operations):
class HtmlTempletOperations (Operations):  # could be HtmlCompileOperations
  '''
  Takes an .html-extension yaml subtree, and compiles it to a Django html template.
  Either compiles from a file ("compile"), or from yaml-inline jade, markdown, or minaml / shpaml.
  Future enhancements include:
  - output of more templating languages
  - integration of direct db-inserts and near-JIT compiling from Django signals
  - integration of stylus, less/sass, coffee etc into direct block references in the generated template
  '''
  notice = '''\

{#  WARNING: GENERATED FILE - EDITS WILL BE LOST  #}
{#  GENERATED FROM: %s on %s  #}

'''
  def css (self, context, css_file):  # sass, less, etc
    raise Exception ('NYI')

  def minaml (self, context, template_code):
    self.template = convert_text (template_code)

  def jade (self, context, template_code):
    self.template = jade2django (template_code)

  def stylus (self, context, template_code):
    self.styles = stylus_compile (template_code) # 'self.styles' not used yet

  def less (self, context, template_code):
    self.styles = less_compile (template_code) # not used yet

  def sass (self, context, template_code):
    self.styles = sass_compile (template_code) # not used yet

  def coffee (self, context, template_code):
    self.javascripts = coffee_compile (template_code)  # not used yet

  def markdown (self, context, template_code):
    self.template = markdown_render (template_code)

  def compile (self, context, fname):
    self.source_fname = fname
    ext = fname.split ('.') [-1]

    if ext == 'minaml':  # TODO: jade, stylus, sass, less, md, etc, shpaml :-)
      print templates_path, fname
      self.minaml (None, open (templates_path + fname).read())
    else:
      raise Exception ('NYI')

  def finalize (self):
    fname = self.root

    if hasattr (self, 'source_fname'):
      notice = self.notice % (self.source_fname, dt())
    else:
      notice = self.notice % ('%s at line %s' % (map_file, self.map_line), dt())

    if self.template.strip().startswith ('{%'):  # skip 1st line
      l = self.template.split ('\n', 1)
      l.insert (1, notice)
      s = '\n'.join (l)
    else:
      s = notice + self.template

    self.write (s, fname)


class CssCompileOperations (HtmlTempletOperations):  # Compile from stylus, sass, less, etc
  '''
  Takes a .css-extension yaml subtree, and compiles it to css file.
  Either compiles from a file ("compile"), or from yaml-inline less, sass, or stylus code.
  '''
  notice = '''\

/*  WARNING: GENERATED FILE - EDITS WILL BE LOST  */
/*  GENERATED FROM: %s on %s  */

'''

  def stylus (self, context, template_code):
    #print 'BEFORE STYLUS'
    self.template = stylus_compile (template_code)
    #print 'AFTER STYLUS'

  def less (self, context, template_code):
    self.template = less_compile (template_code) # not used yet

  def sass (self, context, template_code):
    self.template = sass_compile (template_code) # not used yet


class HtmlPyqueryOperations (Operations):
  notice = '''\

{#  WARNING: GENERATED FILE - EDITS WILL BE LOST  #}
{#  GENERATED FROM: %s at line %s on %s  #}

'''
  def load (self, context, fname):
    #self.read (context, fname)
    fname = Template (fname).safe_substitute (config)
    with open (fname) as f:
      lxml_etree = html5lib.parse(f, treebuilder="lxml", namespaceHTMLElements=False)
      self.d = pq (lxml_etree.getroot())  # d => dollarsign-equiv, for jquery/pyquery css selector
    self.scripts = ''  # cheapo init
    self.styles = ''

  def remove (self, dselector, dummy):
    dselector.remove()

  def remove_filtered (self, dselector, filtered):
    dselector.filter(lambda i, this: pq(this).text().strip().startswith(filtered)).remove()

  def remove_others (self, dselector, subselector):
    "This does not work, as pyquery's d.not_ does not appear to work at all."
    print 'DSELECTOR', dselector
    print 'SUBSELECTOR', subselector
    print 'DSELECTOR NOT', dselector.not_ (subselector) # this does not work
    print 'SUBSELECTED', dselector (subselector) # this works
    #print 'SUBSELECTED NOT', dselector (subselector).not_('') # fault
    dselector.not_ (subselector).remove()
    print 'DSELECTOR after remove', dselector

  def innerHtml (self, dselector, replacement):  # renamed from jquery/pyquery 'html', to avoid conflict with selector
    dselector.html (replacement)

  def outerHtml (self, dselector, replacement):
    #dselector.outerHtml (replacement)
    dselector.replace_with(replacement)
    #parent=dselector.parents()[0]
    #dselector.remove()
    #parent.append (pq (replacement))
    #pq (replacement).append_to (parent)
    #parent.extend (pq (replacement))

  def ensure_old (self, dselector, kwlist):  # creates dups of dicts with multiple attrs
    def check_present(k,v):
      for tag in dselector:
        if k.lower() in tag.attrib and tag.attrib [k] == v.lower:
          return True
    for d in kwlist:
      for k,v in d.items():
        if not check_present (k,v):
          last = [dselector.eq(x) for x in range(dselector.length)] [-1]
          e = dselector[0].makeelement(dselector[0].tag, d)  # JJW 10/24/15 {k:v})
          e.tail = '\n'
          last.after (pq (e))

  def ensure (self, dselector, kwlist):
    "ensure: Takes list of attribute dictionaries and ensures they are in the tags selected"
    def check_present(d):
      for tag in dselector:
        for k,v in d.items():
          if not (k.lower() in tag.attrib and tag.attrib [k] == v.lower):
            return False
      return True
    kwlist.reverse()  # otherwise they end up in the HTML in reverse order listed in the YAML - so follow the POLS
    for d in kwlist:
      if not check_present (d):
        last = [dselector.eq(x) for x in range(dselector.length)] [-1]
        e = dselector[0].makeelement(dselector[0].tag, d)  # JJW 10/24/15 {k:v})
        e.tail = '\n'
        last.after (pq (e))

  def attr (self, dselector, replacement):
    for k,v in replacement.items():
      v = Template (v).safe_substitute (config)
      dselector.attr (k,v)

  def removeAttr (self, dselector, data):
    dselector.removeAttr (data)

  def addClass (self, dselector, data):
    if not isinstance (data, (list, tuple)):
      data = [data]
    for d in data:
      dselector.addClass (d)

  def removeClass (self, dselector, data):
    if not isinstance (data, (list, tuple)):
      data = [data]
    for d in data:
      dselector.removeClass (d)

  def attr_prefix (self, dselector, replacement):
    for k,v in replacement.items():
      v = Template (v).safe_substitute (config)
      # nope: e is int: dselector.each (lambda e: e.attr (k,v + e.attr(k)))
      for e in dselector.items():
        if e.attr (k):
          e.attr (k,v + e.attr(k))

  def before (self, dselector, insertion):
    "Inserts a string before the start of the dselector (text, tag, anything)"
    dselector.before ('\n' + insertion + '\n')

  def after (self, dselector, insertion):
    "Inserts a string after the end of the dselector (text, tag, anything)"
    dselector.after ('\n' + insertion + '\n')

  def prepend (self, dselector, insertion):
    "Prepends a string to the start of the dselector (text, tag, anything)"
    dselector.prepend ('\n' + insertion + '\n')

  def append (self, dselector, insertion):
    "Appends a string to the end of the dselector (text, tag, anything)"
    dselector.append ('\n' + insertion + '\n')

  def append_tag (self, dselector, insertion):
    "Appends a tag and contents (k,v of insertion dict) to the dselector"
    for k,v in insertion.items():
      dselector.append ('<%s>\n%s</%s>' % (k,v,k)) # 1st, for style - should do less, sass, stylus, etc

  def merge_scripts (self, dselector, script):
    '''
    Adds a script (inline or src) to list of scripts for this page (saves state in self.scripts)
    Should implement YAML_HTML here, refd scruz boardwalk walk May, 2015.
    Format is src=<url> for file-based, or just inline javascript. Javascript tags will be added.
    '''
    self.scripts += '\n' + script

  def merge_styles (self, dselector, style):
    '''
    Adds a style (inline or href) to list of scripts for this page (saves state in self.scripts).
    Should implement YAML_HTML here, refd scruz boardwalk.
    Format is href=<url> for file-based, or just inline styles. CSS link tag will be added.
    '''
    self.styles += '\n' + style

  def append_scripts (self, dselector, dummy):
    '''
    Appends scripts to dselector - right now, just passes thru script body, and tagifies lines starting wtih "src=".
    Could support CoffeeScript, parse the tag more thoroughly, check for dups, etc - JJW
    TODO:
      detect dups and merge - eg, jquery, owl carousel, etc
      detect version conflicts - jquery, etc - integrate w/Bower?
      pass thru untouched iff startswith "<"
      append to js file if data parm is present and not empty
    '''
    if not self.scripts.strip():  # return
      self.scripts = '/* None */' # needed to have a matching tag at the end, after template blocks, etc, so it's parsed correctly

    lines = self.scripts.split ('\n')
    links = []

    for i, line in enumerate (lines):
      toks = line.lower().split ('=', 1)
      if toks [0].strip() == 'src':  # RISK - actual js setting a 'src' var!  mnight be better to use full "<script ..."
        line = lines.pop (i)
        links += ['<script %s type="text/javascript"></script>' % line]

    s = '\n'.join (['\n\n<!-- Appended scripts -->\n'] + links + ['\n<script>'] + lines + ['</script>'])
    dselector.append (s)
    self.scripts = ''  # cheap way to make idempotent, but means you can't use in multiple saves..

  def append_styles (self, dselector, dummy):
    '''
    Appends styles to dselector - right now, just passes thru inline styles, and link-tagifies lines starting wtih "href=".
    media=<screen or ..> are OK, as long as they're at the end.  type= and rel= are added automatically as they are invariant.
    Could support Stylus, Sass, Less, parse the tag more thoroughly, check for dups, etc - JJW
    Todo:
      pass thru untouched iff startswith "<"
      append to css file if data parm is present and not empty
    '''
    if not self.styles.strip():  # return
      self.styles = '/* None */' # needed to have a matching tag at the end, after template blocks, etc, so it's parsed correctly

    lines = self.styles.split ('\n')
    links = []

    for i, line in enumerate (lines):
      toks = line.lower().split ('=', 1)
      if toks [0].strip() == 'href':
        line = lines.pop (i)
        links += ['<link %s type="text/css" rel="stylesheet">' % line]

    s = '\n'.join (['\n\n<!-- Appended styles -->\n'] + links + ['\n<style>'] + lines + ['</style>'])
    dselector.append (s)
    self.styles = ''  # cheap way to make idempotent, but means you can't use in multiple saves..

  def merge (self, dselector, data):
    "This is of limited usefulness, see notes - originally intended for styles & scripts, which are now implemented directly - JJW"
    decl_name = data.pop ('declaration')

    if not decl_name in declarations:
      declarations [decl_name] = OrderedDict()

    decl_dict = declarations [decl_name]

    for k,v in data.items():
      if k in decl_dict:
        decl_dict [k] += '\n' + v
      else:
        decl_dict [k] = v

  def empty (self, dselector, dummy):
    "Empties the contents of the dselector node or nodes"
    dselector.empty()


  #def wrap_compress_css (self, dselector, tags):
  #  s = '{% compress css %}\n%s\n{% endcompress %}' % '\n'.join ([t.outerHtml() for t in tags])
  #  dselector.append ()

  # this works, kind of, needs work w/LFs -
  #def wrap_command (self, dselector, cmd):  # assumes 2-part cmd, eg 'compress css' or 'block content'
  #  s = '\n{%% %s %%}\n%s\n{%% end%s %%}' % (cmd,
  #        '\n'.join ([t.after('\n').outerHtml() for t in dselector.items()]),
  #        cmd.split()[0])
  #  dselector.parent().append (s)

  # nope
  #def wrap_command (self, dselector, cmd):  # assumes 2-part cmd, eg 'compress css' or 'block content'
  #  s = '\n{%% %s %%}\n%s\n{%% end%s %%}' % (cmd,
  #        '\n'.join ([t.each (lambda e: e.tail('\n')).outerHtml() for t in dselector.items()]),
  #        cmd.split()[0])
  #  dselector.parent().append (s)

  # or this leaves them in place :)
  def wrap_command (self, dselector, cmd):  # assumes 2-part cmd, eg 'compress css' or 'block content'
    l = [t for t in dselector.items()]
    if l:
      l[0].before ('\n{%% %s %%}\n' % cmd)
      l[-1].after ('\n{%% end%s %%}\n' % cmd.split()[0])

  def cut (self, dselector, fname):
    '''cut - copies inner html to clipboard, then blanks it out.
    Really, the default should be to cut the outerHtml (matches 'save' semantics), and rename cut to cutInner.
    Minimalist state kept via Cut/Paste semantics.  Easier than Mark/Move/Copy semantics, for now - JJW.'''
    self.clipboard = dselector.html()
    #if trace: print 'CUT:', self.clipboard [:20]
    dselector.html('')

  def cutOuter (self, dselector, fname):
    '''cutOuter - copies outerHtml to clipboard then removes the dselector.
    Really, the default should be to cut the outerHtml (matches 'save' semantics), and rename cut to cutInner.
    Minimalist state kept via Cut/Paste semantics.  Easier than Mark/Move/Copy semantics, for now - JJW.'''
    self.clipboard = dselector.outerHtml()
    if trace: print 'CUT OUTER:', self.clipboard [:20]
    dselector.remove()

  def paste (self, dselector, fname):
    "Minimalist state kept via Cut/Paste semantics.  Easier than Mark/Move/Copy semantics, for now - JJW."
    dselector.html (self.clipboard)
    # if trace: print 'PASTE:', dselector

  def loop (self, dselector, data):
    '''
    This is an important aaction function - it implements 'dzip', or loop, which can avoid
    completely rewriting or reimplementing large loop sections in some templateing language,
    such as Django's template language, Jade, Shpaml / Minaml, etc.

    It accepts only a couple of required parameters, 'for', which is the tail of a for
    expression, and 'repeat', which is the html to be looped, complete with replacements.

    Optional params are 'first' and 'last', which can be slightly alternate css classes,
    etc for these two edge cases.

    You build these snippets, and choose where, by using the css selector syntax to specify
    what you want replaced, and where, and then use 'repeat', 'first', and 'last' to tell
    the loop function to clone these into the loop expression.  See the examples for ideas.

    The loop semantics are:

    first only: if forloop.first then first else repeat
    last only: if forloop.last then last else repeat
    neither: repeat
    both: if both then once elif first elif last else

    For now, the 'both' case is not implemented, as it would require the last one, above,
    plus a 'once' param as well, for the edge case of one item with both first and last set.
    TBD.
    '''
    for_exp = data.pop ('for')
    first = ''
    last = ''
    repeat = ''

    print "LOOP", dselector  # repeat_selector
    print data

    for k,v in data.items():
      if k in ('repeat','first','last'):  # 'once', too
        exec (k + ' = dselector(v).clone()')
        #locals() [k] = dselector(v).clone()  # nope, nfg
      else:
        context = dselector(k)
        print
        print k, 'CONTEXT:', context
        print
        for k2,v2 in v.items():
          print 'K2:', k2
          if k2 in self.actions:
            self.__getattribute__ (k2) (context, v2)
          else:
            raise Exception ('Unknown action:', k2)
          #elif k2 == 'clone' or k2 == 'use':
          #  print 'V2:', v2
          #  loop_parms [v2] = context.clone()

    print 'PARMS:', repeat, first, last, for_exp  # ,once

    if repeat:
      s = "\n{%% for %s %%}" % for_exp
    else:
      raise Exception ('Repeat required in dzip / loop')

    # see docstring - only doing first & last, here for now, both unsupported ATM

    if first:
      s += "\n  {% if forloop.first %}\n    " + first.outerHtml() + "\n  {% else %}\n    " + repeat.outerHtml() + "\n  {% endif %}"
    elif last:
      s += "\n  {% if forloop.last %}\n    "  + last.outerHtml()  + "\n  {% else %}\n    " + repeat.outerHtml() + "\n  {% endif %}"
    else:
      s += "\n  " + repeat.outerHtml()

    s += "\n{% endfor %}"

    print s
    dselector.html (s)

  dzip = loop  # alternate name, branding :-)


  def extract (self, dselector, fname):
    "This is lower-level, and doesn't call _write, which prepends the template_path and iunescapes the src and href attrs"
    with open (fname, 'w') as f:
      f.write (str (dselector))  #, encoding='utf-8'))

  def show (self, dselector, dummy):
    for e in dselector:
      print e

  def show_attr (self, dselector, data):
    for e in dselector:
      #print 'http://codepeoples.com/tanimdesign.net/thsop-v-1.3/gray/' + e.attrib [data]
      print e.attrib.get (data, '(No attr)')

  def _save (self, content, fname):
    s = content
    # huge kluge:
    # workaround for lxml.etree serializer gratuitously escaping tag attrs which contain URLs
    s = s.replace ('%7B%7B%20', '{{ ').replace ('%20%7D%7D', ' }}') \
         .replace ('7B7B', '{{').replace ('%7D%7D', '}}') \
         .replace ('%7B%%20', '{% ').replace ('%20%%7D', ' %}') \
         .replace ('%7B%', '{%').replace ('%%7D', '%}') \
         .replace ('%20', ' ') # even more dangerous...  perhaps should just url-unescape the whole str..
         # eg, {% url 'contact' %} - should put both types of quotes in repl, but then would double..
    self.content = s
    self.write (s, fname)

  def save (self, dselector, fname):
    #u''.join ([lxml.html.tostring (e, encoding=unicode) for e in self.d])
    self._save (self.notice % (map_file, self.map_line, dt()) + dselector.outerHtml(), fname)

  def save_doc (self, dselector, fname):  # really should refactor to use %20 etc escapes, etc
    self._save (u'<!DOCTYPE html>\n' +
      #self.notice % (map_file, self.map_line) + dselector.outerHtml(), fname)
      self.notice % (map_file, self.map_line, dt()) + self.d.outerHtml(), fname)

  def save_template_once (self, dselector, fname):
    "Save partial template for later editing; don't overwrite!"
    if os.path.exists (templates_path + fname):
      if trace: print 'Not overwritten:', fname
      return
    ext = fname.lower().split ('.') [-1]
    s = dselector.outerHtml()
    if ext == 'minaml':
      s = convert_to_shpaml (s)
    else:
      print 'NYI'
    self._save (s, fname)

  def minaml (self, dselector, template_code):
    dselector.html (convert_text ('\n' + template_code))

  def minaml_replace (self, dselector, template_code):  # does NOT work for 'html' (top node) - no parent
    dselector.replaceWith (convert_text ('\n' + template_code))

  def jade (self, dselector, template_code):
    dselector.html (jade2django (template_code))

  def stylus (self, dselector, template_code):
    dselector.html (stylus_compile (template_code))

  def markdown (self, dselector, template_code):
    dselector.html (markdown_render (template_code))

  def unknown (self, op, data):
    self.context = self.d (op)  # d => dollar-sign-equiv, for jquery/pyquery css selector, also the d in dzip

    if trace & 2:
      try:
        print 'IN HPO UNKNOWN:', op, data
      except UnicodeEncodeError:
        print 'ANNOYING UNICODE BS 3'

    # could check for declarations on left side here, or 'None' on right

    if isinstance (data, (str, unicode)):  # remove, call a decl, etc
      if data in declarations:
        self.apply (self.context, declarations [data])
      elif data in self.actions:
        self.apply (data, None)
      else:
       raise Exception ('Operation not in actions or declarations:' + data)
    else:
      for k,v in data.items():
        if trace:
          print 'IN HPO UNKNOWN at line %s CALLING:' % (yaml_lines [k]), k
          if trace & 2:
            try:
              print 'WITH DATA:', v
            except UnicodeEncodeError:
              print 'ANNOYING UNICODE BS'
        self.apply (k, v)  # (op, data)

  def finalize (self):
    self.save_doc (self.d, self.root)


class HtmlPyqueryExtractOperations (HtmlPyqueryOperations):
  def __init__ (self, fname, data):
    super(HtmlPyqueryExtractOperations, self).__init__(fname, data)
    self.load (None, fname)

  def finalize (self):  # no save, since this class is just for extract -
    # could refactor whole stack into a v3 implem at some point - JJW
    pass


### Factory-style meta-constructor:

def construct_operations (k, v):  # k,v = root-level node
  ext = k.lower().split ('.') [-1]

  if ext == 'css':
    if v.keys() [0] == 'read':
      return FileOperations (k, v)
    elif v.keys() [0] == 'load':
      return CssOperations (k, v)
    elif v.keys() [0] == 'stylus':
      return CssCompileOperations (k, v)
  elif ext == 'html':
    #if isinstance (v, (str, unicode)) or 'minaml' in v:
    if k.startswith ('$theme_downloaded_path'):
      return HtmlPyqueryExtractOperations (k, v)  # extract only, no finalize / save
    elif v.keys() [0] in ['minaml', 'compile']:
      return HtmlTempletOperations (k, v)
    elif v.keys() [0] == 'load':
      return HtmlPyqueryOperations (k, v)
    else:
      raise Exception ('NYI')
  elif ext == 'yaml':
    return YamlOperation (k, v)


#### Main

if __name__ == '__main__':
  YamlOperation ('themes.yaml', None)()


