docker build -t budget-image .

docker run --name budget-app -v D:\Budget\Appli\db:/usr/src/app/db -v D:\Budget\Appli\db_users:/usr/src/app/db_users -p 5000:5000 budget-image