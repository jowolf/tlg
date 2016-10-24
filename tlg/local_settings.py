# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "h&=@g-m76&o9=6vb0#cm!f*ajhw+f)arqdki+%r_fkzp*=%tl6"
NEVERCACHE_KEY = "(fj@$7qu7c22ffz#amn9+kskaby_=se7hmwj3xww@jy32re#8g"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "tlg.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

INSTALLED_APPS = (
    #'apps.realestate',
    'apps.home',
  ) + INSTALLED_APPS

TEMPLATES [0] ['OPTIONS'] ['context_processors'] += ['apps.home.context_processors.is_home',]

#BLOG_URLS_USE_DATE = True
BLOG_URLS_DATE_FORMAT = 'month'
BLOG_USE_FEATURED_IMAGE = True
ADMIN_THUMB_SIZE = '36x36'

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = ["127.0.0.1"]

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

FABRIC = {
     "DEPLOY_TOOL": "rsync",  # Deploy with "git", "hg", or "rsync"
#     "SSH_USER": "",  # VPS SSH username
     "HOSTS": ALLOWED_HOSTS,   # [""],  # The IP address of your VPS
     "DOMAINS": ALLOWED_HOSTS,  # Edit domains in ALLOWED_HOSTS
     "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
     "LOCALE": "en_US.UTF-8",  # Should end with ".UTF-8"
#     "DB_PASS": "",  # Live database password
     "ADMIN_PASS": "pw4admin",  # Live admin user password
     "SECRET_KEY": SECRET_KEY,
     "NEVERCACHE_KEY": NEVERCACHE_KEY,
}
