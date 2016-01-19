import os, sys, subprocess

from urllib import urlopen
from time import strftime

trace = 1

def dt():
  return strftime("%Y-%m-%d at %H:%M:%S %Z(GMT%z)")   # '2015-05-26 at 16:14:54 PDT(GMT-0700)'

def ensure_dirs (f):
  d = os.path.dirname(f)
  if d and not os.path.exists(d):
    os.makedirs(d)

def my_slugify_url (s):
  s = s.lower().replace ('http://', '').replace ('www.', '').replace ('/', '-')
  return s # slugify (unicode (s))

def ensure_local (url, path):
  fname = path + my_slugify_url (url)
  ensure_dirs (fname)
  if os.path.exists (fname):
    return open (fname).read()
  
  s = urlopen (url).read()
  with open (fname, 'w') as f:
    f.write (s)
    f.flush()

  return s

''' above should be ensure_local_file
def ensure_files (url):
  fname = path + my_slugify_url (url)
  ensure_dirs (fname)
  if os.path.exists (fname):
    return open (fname).read()
  
  s = urlopen (url).read()
  with open (fname, 'w') as f:
    f.write (s)
    f.flush()

  return s
'''

class Meta():  # could make an ABC for this, with soft-attr handling
  def ensure (name, content):
    pass
    #if itsthere:
    #  modify-it
    #else:
    #  add-it

def stylus_compile (source):
    args = 'stylus'  # shlex.split("%s " % getattr (settings, 'STYLUS_EXECUTABLE', 'stylus'))

    p = subprocess.Popen (args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, errors = p.communicate(source.encode("utf-8"))

    if trace:
        print out, errors

    out = out.strip()

    if out:
        return out.decode("utf-8")
    elif errors:
        return errors.decode("utf-8")  # maybe raise an exception here?

    return u"Unknown error"


