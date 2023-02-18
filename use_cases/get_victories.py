import requests

res = requests.get("http://fastapifftt.thorigne-tt.net/matches/3524012",timeout=60)
for match in res.json():
    if match['victoire'] == 'V':
        print(f"{match['nom']} : {match['classement']} points")
        