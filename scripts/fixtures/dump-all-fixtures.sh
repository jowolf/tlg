## Run this in prod, then check in, to update to the latest full db

## These next three (from eRacks) are the 'all' dump to restore the full db - JJW 9/29/16

./manage.py dumpdata --format yaml --natural-primary --natural-foreign auth.permission >fixtures/auth.permission.yaml
./manage.py dumpdata --format yaml --natural-primary                   contenttypes    >fixtures/contenttypes.yaml

./manage.py dumpdata --format yaml --natural-foreign -e auth.permission -e contenttypes -e sessions >fixtures/all.yaml

exit

old, from eracks - may need for tlg testing setup soon

./manage.py dumpdata --format=yaml home         >apps/home/fixtures/home-all.yaml
#./manage.py dumpdata --format=yaml quickpages   >fixtures/quickpages-all.yaml 

## These have to be dumped in a certain oprder with certain options to not create a snafu on load
./manage.py dumpdata --format=yaml --exclude auth.permission auth >fixtures/auth-all.yaml

