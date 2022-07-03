docker build -t budget-image .

docker run -it --rm --name budget-app -v D:\Budget\Appli\db:/usr/src/app/db -p 5000:5000 budget-image