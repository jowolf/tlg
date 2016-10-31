
from mezzanine.pages.models import Page


def is_home(request):
    """
    Returns True iff we are on the home page - the Mezzanine
    on_home templatetag doesn't work in the header - it
    erroneously returns False, even while returning True
    in the body, on thge same page.
    """
    #from pprint import pprint
    #pprint (request.__dict__)
    page = getattr(request, "page", None)
    #print 'PAGE:', page  # None
    #print 'CURRENT_APP', request.resolver_match  # current_app
    return dict (is_home = request.path=='/')
