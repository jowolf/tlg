# To create relative symlinks here:

ln -s ../../../themes/unify/HTML/assets/ unify-assets

# Don't forget to:

./manage.py collectstatic -l 

# See matching urlpatterns in urls.py (and soon in nginx conf)
#
# j
