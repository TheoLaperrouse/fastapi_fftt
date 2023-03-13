import requests

res = requests.get("http://fastapifftt.thorigne-tt.net/matches/proA", timeout=60)
for player in res.json():
    print(f'{player[0]} : {player[1]["vict"]}/{player[1]["matches"]} ' \
        f'({player[1]["win_ratio"]:.2f}%)')
