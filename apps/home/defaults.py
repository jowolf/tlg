from mezzanine.conf import register_setting

#register_setting (
#    name="SITE_LOGO",
#    label="Site Logo",
#    description="The Logo that appears with Site Title and Tagline.",
#    editable=True,
#    default='<img src="/img/logo.png" alt="{{ settings.SITE_TITLE }}", title="{{ settings.SITE_TITLE }}">',
#)

register_setting (
    name="ORG_LOGO",
    label="Organization Logo",
    description="The Logo that appears for the organization / domain, along with the Site Title and Tagline.",
    editable=True,
    default='<img src="/img/logo.png" alt="{{ settings.SITE_TITLE }}", title="{{ settings.SITE_TITLE }}">',
)

register_setting (
    name="ORG_THEME_COLOR",
    label="Organization Theme Color",
    description="The Theme Color that appears for the organization / domain.",
    editable=True,
    default='default',
    choices = (
        ('aqua',        'Aqua'),
        ('blue',        'Blue'),
        ('brown',       'Brown'),
        ('dark-blue',   'Dark Blue'),
        ('dark-red',    'Dark Red'),
        ('default',     'Default (Green)'),
        ('light-green', 'Light Green'),
        ('light',       'Light'),
        ('orange',      'Orange'),
        ('purple',      'Purple'),
        ('red',         'Red'),
        ('teal',        'Teal'),
      )
)

register_setting (
    name="ORG_ABOUT1",
    label="About Organization blurb 1",
    description="A short, meaningful blurb about the organization / domain - a little longer than a tagline.",
    editable=True,
    default="About your nifty boffo Organization's accomplishments, strides, trials, and tribulations goes here",
)

register_setting (
    name="ORG_ABOUT2",
    label="About Organization blurb 2",
    description="A second short, meaningful blurb about the organization / domain.",
    editable=True,
    default="More about your nifty boffo Organization's wonderful and notable accolades and laudable achievements here, too",
)

register_setting (
    name="ORG_SLIDER_IMG",
    label="Organization Slider Image",
    description="The full-width slider image displayed on the home page for the organization. 2046x427 by default, 2k width suggested.",
    editable=True,
    default="../img/bg.jpg",
)



# You must also put them below if you want them to be usable in templates - see also
# https://github.com/stephenmcd/cartridge/blob/master/cartridge/shop/defaults.py
# https://groups.google.com/forum/#!topic/mezzanine-users/aVUCLKQyHcQ
register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description="Sequence of setting names available within templates.",
    editable=False,
    default=(
        "ORG_LOGO",
        "ORG_THEME_COLOR",
        "ORG_ABOUT1",
        "ORG_ABOUT2",
        "ORG_SLIDER_IMG",
      ),
    append=True,
)

