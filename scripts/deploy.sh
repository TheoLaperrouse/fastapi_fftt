cd fastapi_fftt
git pull
sudo docker rm -f fastapi_fftt
sudo docker rm -f redis
sudo docker build . -t fastapi_fftt
sudo docker run -d --name redis -p 6379 redis 
sudo docker run -d -p 80:8000 --name fastapi_fftt fastapi_fftt