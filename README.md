# FastAPI FFTT

FastApi / Uvicorn Backend deployed with EC2 / Route53

## Explanation

Use the FFTT (France Table Tennis Federation) Api to get Table Tennis players and their results.

Use pylint for static code analysis

Deployed with AWS EC2 here : 

http://fastapifftt.thorigne-tt.net/docs

CI to lint and redeploy on push with Github secrets

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

### Use Cases :

Script Python (in use_cases folder) :
- Get victories of a player :
```python
res = requests.get("http://fastapifftt.thorigne-tt.net/matches/3524012",timeout=60)
for match in res.json():
    if match['victoire'] == 'V':
        print(f"{match['nom']} : {match['classement']} points")
```
- Get ProA Stats :
```python
res = requests.get("http://fastapifftt.thorigne-tt.net/proA", timeout=60)
for player in res.json():
    print(f'{player[0]} : {player[1]["vict"]}/{player[1]["matches"]} ' \
        f'({player[1]["win_ratio"]:.2f}%)')

```
