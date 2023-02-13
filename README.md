# FastAPI FFTT

## Quick Start

- Install dependencies :
```sh
pip install -r requirements.txt
```

- Set up a .env file with theses keys:
```
ID_FFTT=""
KEY_FFTT=""
```

- Run app :
```sh
python3 src/main.py
```

- Run app in dev mode :
```sh
uvicorn src.main:app --reload
```

- Use with Docker :
```sh
docker build . -t fastapi_fftt 
```
```sh
docker run fastapi_fftt -p 8000:8000
```
