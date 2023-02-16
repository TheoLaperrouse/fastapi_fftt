# FastAPI FFTT

FastApi / Uvicorn Backend deployed with EC2 / Route53

## Explanation

Use the FFTT (France Table Tennis Federation) Api to get Table Tennis players and their results.

Use pylint for static code analysis

Deployed with AWS EC2 here : 

http://fastapifftt.thorigne-tt.net/docs

## Quick Start

- Set up a .env file with theses keys:
```
ID_FFTT=""
KEY_FFTT=""
MJ_APIKEY_PUBLIC=""
MJ_APIKEY_PRIVATE=""
```

### Python

- Install dependencies :
```sh
pip install -r requirements.txt
```

- Run app in dev mode :
```sh
uvicorn src.main:app --reload
```
### Docker 

- Build the Docker image :
```sh
docker build . -t fastapi_fftt 
```

- Run the Docker Image to deploy it on port 80 :
```sh
docker run -d -p 80:8000 fastapi_fftt 
```
