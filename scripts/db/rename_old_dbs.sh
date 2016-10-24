# This script renames the old dbs and keeps three backups in old/ - 

#echo current $0
#exit

# This should be run from the root of the repo, eg ./scripts/rename_old_dbs.sh

rm old/tlg-old3.db

mv old/tlg-old2.db old/tlg-old3.db
mv old/tlg-old1.db old/tlg-old2.db
mv old/tlg-old.db  old/tlg-old1.db
cp tlg.db          old/tlg-old.db
