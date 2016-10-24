echo SET UP DB - BACKUP OLD
./scripts/db/rename_old_dbs.sh

echo SET UP DB - CREATE
./scripts/db/create-db.sh

echo SET UP DB - ADMIN USERS
./scripts/db/ensure_admin_users.sh

# this step done by mezz create db above
#echo SET UP DB - MIGRATE
#./manage.py migrate

echo SET UP DB - LOAD FIXTURES
./manage.py loaddata fixtures/contenttypes.yaml 2>&1
./manage.py loaddata fixtures/auth.permission.yaml 2>&1
./manage.py loaddata fixtures/all.yaml 2>&1
#./manage.py loaddata fixtures/quickpages-all.yaml

echo SET UP DB DONE
