#import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to

from apps.utils import host_theme_media_path

class HomePage (Page, RichText):
    '''
    A page class for the data in the home page
    '''
    heading                 = models.CharField ( max_length=200, help_text="The heading under the icon blurbs")
    subheading              = models.CharField ( max_length=200, help_text="The subheading just below the heading")
    featured_works_heading  = models.CharField ( max_length=200, default="Featured Works")
    #featured_portfolio     = models.ForeignKey("Portfolio", blank=True, null=True, help_text="If selected items from this portfolio will be featured on the home page.")
    content_heading         = models.CharField ( max_length=200, default="About us!")
    latest_posts_heading    = models.CharField ( max_length=200, default="Latest Posts")

    def call_to_action (self):
        return self.blurbs.filter (usage = 'call-to-action') [0]

    def row_of_three (self):
        return self.blurbs.filter (usage = 'row-of-three')

    def row_of_four (self):
        return self.blurbs.filter (usage = 'row-of-four')

    def client_icon_list (self):
        return self.blurbs.filter (usage = 'client-icon-list')

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")

usages = (
    ('slider', 'slider'),
    ('call-to-action', 'call-to-action'),
    ('row-of-three','row-of-three'),
    ('row-of-four','row-of-four'),
    ('two-plus-one','two-plus-one'),
    ('client-icon-list', 'client-icon-list'),
    ('slider-overlay-left','slider-overlay-left'),
    ('slider-overlay-right','slider-overlay-right'),
    ('parallax-bottom','parallax-bottom'),
)

# See docs in apps.utils.host_theme_media_path

#blurb_path = host_theme_media_path
#blurb_path.suffix = 'blurb'
def blurb_path(): return host_theme_media_path ('blurb')

class ImageBlurb (Orderable):
    '''
    Content snippet with title, image, link, and usage - on a HomePage
    '''
    homepage = models.ForeignKey (HomePage, related_name="blurbs")
    image = FileField (verbose_name = _("Image"),
        #upload_to = upload_to ("theme.ImageBlurb.image", "images"),
        upload_to = blurb_path,
        format = "Image", max_length = 255)
    title = models.CharField (max_length = 200)
    content = models.TextField()
    html = models.TextField (blank=True, help_text="Extra html or alternative to Image field - eg, maps embed, FA Icon, subscribe form, download / contact button, etc")
    link = models.CharField ( max_length = 2000, blank = True, help_text="Optional, if provided clicking the blurb will go here.")
    usage = models.CharField ( max_length = 20, choices = usages)

# Maybe ActionBlurb? with action text / form to put on a button and show the form for - JJW 11/15/16
# row-of-three: title content icon-class (metadata)

# See docs in apps.utils.host_theme_media_path

#slider_path = host_theme_media_path
#slider_path.suffix = 'slider'
def slider_path(): return host_theme_media_path ('slider')

# Might be able to combine this with blurb at some point

class Slide (Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey (HomePage, related_name="slides")

    image = FileField (verbose_name =_("Image"),
        #upload_to = upload_to ("theme.Slide.image", "slider"),
        #upload_to = os.path.join (host_theme_name(), "slider"),
        upload_to = slider_path,
        format = "Image", max_length = 255, null = True, blank = True)
    title = models.CharField (max_length = 200)  # Heading or H2
    description = models.TextField()    # description or p
    html = models.TextField (blank=True, help_text="Alternative to Image field - eg, Video embed, etc") # could use similar idea for FA icon
    link = models.CharField (max_length = 2000, blank = True, help_text="Optional, if provided clicking the image or blurb will go here.")


""" examples

maybe slide should have an h2, etc, in addition to link, tagline

class Slide (Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey (HomePage, related_name="slides")
    image = FileField (verbose_name =_("Image"),
        upload_to = upload_to ("theme.Slide.image", "slider"),
        format = "Image", max_length = 255, null = True, blank = True)


class IconBlurb (Orderable):
    '''
    An icon box on a HomePage
    '''
    homepage = models.ForeignKey (HomePage, related_name="blurbs")
    icon = FileField (verbose_name = _("Image"),
        upload_to = upload_to ("theme.IconBlurb.icon", "icons"),
        format = "Image", max_length = 255)
    title = models.CharField (max_length = 200)
    content = models.TextField()
    link = models.CharField ( max_length = 2000, blank = True, help_text="Optional, if provided clicking the blurb will go here.")


class Portfolio (Page):
    '''
    A collection of individual portfolio items
    '''
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")
"""
