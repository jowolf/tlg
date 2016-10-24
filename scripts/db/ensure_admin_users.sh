# This script creates django superusers 

echo Creating joe
./manage.py createsuperuser --user joe --email joe@thelibregroup.com

echo Creating admin
./manage.py createsuperuser --user admin --email joe@eracks.com
