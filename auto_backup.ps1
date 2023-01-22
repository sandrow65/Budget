#docker exec -it db mysqldump --databases BUDGET --result-file=dump_test.sql
#docker cp db:/dump_test.sql ./db


docker run --rm -v appli_copie_mydb:/dir1 -v mysql-db-backup:/dir2 alpine tar -cf backup.tar /dir1 && cp -r /backup.tar /dir2