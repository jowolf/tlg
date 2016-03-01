from mezzanine.conf import register_setting

register_setting (
    name="SITE_LOGO",
    label="Site Logo",
    description="The Logo that appears with Site Title and Tagline.",
    editable=True,
    default='<img src="/img/logo.png" alt="{{ settings.SITE_TITLE }}", title="{{ settings.SITE_TITLE }}">',
)
