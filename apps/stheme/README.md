Overview
========

In web development, it's usually tough to maintain an object-oriented perspective of the various bits and pieces that one uses to assemble a website.

One of these major challenges, is the fiddly and annoying task of keeping track of all the bits and pieces that go together, and their dependencies. 

- Which CSS and which JavaScripts are required for a given HTML snippet or widget to work?
- Which other assets and images go with those widgets? 
- Which database objects (and the corresponding lists thereof) are going to be displayed by the given widget?
- Which widgets require other widgets, frameworks, foundations, etc?

Although it is true that a good IDE could conceivably keep track of all this or most of this, and make life easier, the fact remains that there are far more benefits to group these things together into "objects" with resources and dependencies tied together, going forward - the IDE appraoch is known as "Integration at the glass", and is fraught with problems - none the least of which is, you're WOAP (WithoUt A Paddle) if you're not using the IDE. :-)

Further complicating this picture, is the fact that each page is different, with different dependencies, and some developers just give up, and put everything in all their pages (and their home page) so they don't have to work through all these issues, thus bloating their pages, as well as making debugging much more difficult ("Did I hit this JS code?  Am I using this CSS?  Where it is used?) and so forth.

Even though caching practices on the client may minimize the additional burden, it's still messy, and affects
page load time, debugging, modularity, and so forth.

And furthermore, templating languages, such as Django's template language, (or the closely related Jinja template language), don't make it easy to keep these things grouped together by CSS,
JS, HTML, or images. 

These templating languages require separate sections for each one, with no standardization of block naming, support for dependencies, inheritance, etc - this is ripe for on automation, or for a better player which helps
organize these things.

Obdjects
========

This __Obdjects__ framework (Note the 'D', like Dj) tries to address many of these problems and issues.  It allows you to define the objects themselves, with the resources and dependencies in one place, and allows us to propagate throughout your html5 and CSS themes, and even generating templates for you with the pieces pre-integrated.

It integrates nicely with Django, and allows you to continue using your existing templates, and migrating as graduylally or incrementally as desired.

Django-stheme
=============

("Django's Theme" - geddit?)


Stheme Engine
=============

Can be pronounced "Steam Engine" :-D


Existing eRacks site widgets
============================

Here is a (likely incomplete) list of legacy eracks partials / snippets / templates and fragments, and their locations, as well as their completed status:

app | template | description | legacy location | new theme usage
----|----------|-------------|-----------------|----------------
bloglets ||||
 | _bloglet_list.html | enumerate Bloglet DB table | now in theme-legacy.yaml at line 19 | lower-right home page 
home |||
 | site.css | Site-specific CSS | now in theme-legacy.yaml at 82 | not used in new themes (they each have their own, called something else)
 | _nav_login.html | Social login icons | now in theme-legacy.yaml at 687 | refactored in new themes, togo in popup?
 | _header_right.html | Main login, cart, oss_logos, email | now in theme-legacy.yaml, theme menu added | refactored, generic-declarations
 | _nav_main.html | Main menu | now in theme-legacy.yaml | refactored, generic-declarations
 | _breadcrumbs.html | location / history trail | now in theme-legacy.yaml | refactored, generic-declarations
 | _footer.html | Fat footer | now in theme-legacy.yaml | refactored, generic-declarations
orders |||
| admin-grid.html | is this used? ||
| cart.html | convert to generated or _partial ||
| _checkout_form.html | convert to generic _partial ||
| checkout.html | convert to generated or _partial ||
| _addr.html | convert to _partial or integrate into yaml ||
| _final_cart.html | convert to page or _partial ||
| confirm.html | convert to generated or _partial ||
| ordered.html | convert to generated or _partial ||
| _email_order.html | convert to generated or _partial ||

  - home.html
    %extends base
    %load cache
    css
    content
    js_bottom

- db-based snippets aka "QuickSnippets":
  - geotrust_seal
  - bbb_horizontal
  - google_plus_tag
  - google_plus_include
  - facebook_like
  - facebook_sdk
  - skype_widget
  - home_page_text_3
  - home_page_text_2
  - home_page_text_1
  - trustwave_siteseal
  - bbb_horizontal_old
  - bbb_vertical
  - right_column
  - social_login_logos
  - os_logos
  - mailing_list
  - nav_login
  - nav_small

