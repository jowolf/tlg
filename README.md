TLG - The Libre Group web site 2016
===================================

Oct 2016
--------

Setup:

- clone this repo (into tlg/ by default)
- cd tlg
- familiarize yourself
- git submodule update --init --recursive
- (or use --recursive arg on above clone)
- cd conf
- virtualenv env
- activate the venv (Important!) . env/bin/activate or use ./go.sh from tlg/
- pip -r requirements.txt
- cd ..
- ./go.sh (activeates venv)
- ./manage.py collectstatic -l
- ./manage.py <whatever>

That's it!

TODO: integrate tlg2, unify, orange, images/sites, tests.py in apps, wercker, split out stheme into theme swicher and yaml processor

External migrations steps required 10/13:
- move repo to home dir (no more mezz or mezzanine - its now in conf/env) in all dev envos
- redo virtualenv and check requirements


Jan 2016
--------

With django's-theme engine (stheme app)

Todo:
- modular settings - move or modify manage.py
- outboard themes
- streamline utils, comments, template-loader, middleware

Goal:  Just the base template for now

JJW 1/18/16
