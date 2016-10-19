## Run this to load a new db from scratch - BE CAREFUL

echo BE CAREFUL - this overwites the entrie database -

exit

** upd for nat keys JJW 9/29

./manage.py loaddata apps/home/fixtures/home-all.yaml
#./manage.py loaddata fixtures/quickpages-all.yaml
./manage.py loaddata fixtures/auth-all.yaml

