# To create these relative symlinks here:

ln -s ../../../themes/unify/HTML/One-Pages/assets/ onepage-assets
ln -s ../../../themes/unify/HTML/One-Pages/RealEstate/assets/ realestate-assets

# Don't forget to:

./manage.py collectstatic -l 

# See matching urlpatterns in urls.py (and soon in nginx conf)
#
# j
