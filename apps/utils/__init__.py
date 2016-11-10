import sys, os

from django.contrib.sites.models import Site

from mezzanine.conf import settings
from mezzanine.utils.sites import current_site_id

trace = 0


def host_theme_media_path (suffix):  # (instance, filename):
    """
    Returns the name of the theme associated with the given host,
      suffixed by a string (typically a field name) - called by
      upload_to in model.

    Patterned after mezzanine.utils.sites.host_theme_path

    Does not follow the specs here:
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.FileField.upload_to
    as Mezzanine has apparently broken this, by mapping upload_to into FileBrowseField.directory,
    which is called without parms.

    Solution:  Use function references with a 'suffix' attr, for example:

    from apps.utils import host_theme_media_path
    ...
    slider_path = host_theme_media_path
    slider_path.suffix = 'slider'
    ...
    class Slide (Orderable):
    ...
        image = FileField (
            verbose_name =_("Image"),
            upload_to = slider_path,  # NOTE: no parens!
            format = "Image", max_length = 255, null = True, blank = True)

    UPDATE: attrs don't work, and it uses the last one set at module load time, the fn references are not first-class objects, only refs.

    Just use a one-line call in the model, and pass is a suffix, eg:

    def slider_path(): return host_theme_media_path ('slider')

    QED. KISS principle.
    """

    # Nope.  need to use attr
    #print 'FUNCTION NAME', host_theme_media_path.__name__

    #suffix = instance.__class__.__name__.tolower()
    #suffix = host_theme_media_path.__name__.split ('_') [-1]
    #suffix = host_theme_media_path.suffix
    if trace: print 'SUFFIX', suffix

    # Set domain to None, which we'll then query for in the first
    # iteration of HOST_THEMES. We use the current site_id rather
    # than a request object here, as it may differ for admin users.
    domain = None

    for (host, theme) in settings.HOST_THEMES:
        if trace: print 'HOST THEME', host, theme
        if domain is None:
            domain = Site.objects.get(id=current_site_id()).domain
            if trace: print 'DOMAIN', domain
        if host.lower() == domain.lower():
            if theme:
                if theme.startswith ('apps.'):
                    theme = theme [5:]
                return os.path.join (theme, suffix)  #, filename)
    return ""
