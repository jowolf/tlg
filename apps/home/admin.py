from django.contrib import admin
#from django.contrib.admin import TabularDynamicInlineAdmin

from mezzanine.core.admin import TabularDynamicInlineAdmin  # BaseTranslationModelAdmin
from mezzanine.pages.admin import PageAdmin

from .models import ImageBlurb, HomePage

#class SlideInline(TabularDynamicInlineAdmin):
#  model = Slide

class ImageBlurbInline(TabularDynamicInlineAdmin):
  model = ImageBlurb

class HomePageAdmin(PageAdmin):
  inlines = (ImageBlurbInline,)  # (SlideInline, IconBlurbline)

admin.site.register(HomePage, HomePageAdmin)
#admin.site.register(Portfolio, PageAdmin)
