from mezzanine.conf import register_setting

register_setting (
    name="SITE_STYLES",
    label="Site Styles",
    description="Extra style tweaks included in the 'extra_css' block in the header (Copy/Paste to edit).",
    editable=True,
    #type="text",
    default='''\
    .footer-logo {
      margin: 17px 0 20px;
      background: white;
      border: 10px solid azure;
      border-radius: 10px;
    }
    ''',
  )

register_setting (
    name="ORG_LOGO",
    label="Organization Logo",
    description="The Logo image that appears for the organization / domain. Use with the Site Title for alt & title.",
    editable=True,
    default='<img src="/img/logo.png" alt="{{ settings.SITE_TITLE }}", title="{{ settings.SITE_TITLE }}">',
)

register_setting (
    name="ORG_PHONE",
    label="Organization Phone Number",
    description="The phone number that appears on the site for the organization / domain - include the '+1'.",
    editable=True,
    default='+1800-555-1212',
)

register_setting (
    name="ORG_TEXTS",
    label="Organization Texting Number",
    description="The phone number for texting that appears on the site for the organization / domain - include the '+1'.",
    editable=True,
    default='+1800-555-1212',
)

register_setting (
    name="ORG_EMAIL",
    label="Organization eMail Address",
    description="The eMail address that appears on the site for the organization / domain.",
    editable=True,
    default='info@example.org',
)

register_setting (
    name="ORG_ADDRESS",
    label="Organization Address Info",
    description="Address info (Multiline) that appears in the footer and on the contact page (Copy/Paste to edit).",
    editable=True,
    default='''\
    Los Gatos, Hayward
    California, US
    ''',
    #Phone: +1-800-555-1212
    #Texts: +1-800-555-1212
    #eMail: info@example.org
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
        "SITE_STYLES",
        "ORG_LOGO",
        "ORG_PHONE",
        "ORG_TEXTS",
        "ORG_EMAIL",
        "ORG_ADDRESS",
        "ORG_THEME_COLOR",
        "ORG_ABOUT1",
        "ORG_ABOUT2",
        "ORG_SLIDER_IMG",
      ),
    append=True,
)

