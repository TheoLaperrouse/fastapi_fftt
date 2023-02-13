from fastapi import FastAPI
import uvicorn
from src.connexion_api import connexion_api

app = FastAPI()


@app.get("/players/{licence}")
def get_player_by_licence(licence: str):
    '''Get player by licence'''
    return connexion_api("xml_joueur", f"licence={licence}")['joueur']


@app.get("/players/club/{num_club}")
def get_players_by_club(num_club: str):
    '''Get players by club num'''
    return connexion_api("xml_liste_joueur", f"club={num_club}")['joueur']


@app.get("/matches/{licence}")
def get_match_by_licence(licence: str):
    '''Get last matches by licence'''
    return connexion_api("xml_partie", f"numlic={licence}")['partie']


@app.get("/teams/{num_club}")
def get_teams_by_club(num_club: str):
    '''Get team by club num'''
    return connexion_api("xml_equipe", f"numclu={num_club}")["equipe"]


@app.get("/proA")
def get_pro_a_stats():
    '''Get pro A statistics'''
    players = {}
    matches = get_matches_poules_by_link(get_pro_a())
    for match in [get_match_by_link(m['lien']) for m in matches]:
        if match:
            for individual_match in match:
                if individual_match and individual_match['ja'] and individual_match['jb']:
                    player_a, player_b = individual_match['ja'], individual_match['jb']
                    print(individual_match)
                    score_a = individual_match.get('score_a', -1) == '1'
                    players[player_a] = players.get(
                        player_a, {'vict': 0, 'matches': 0})
                    players[player_b] = players.get(
                        player_b, {'vict': 0, 'matches': 0})
                    players[player_a]['vict'] += score_a
                    players[player_b]['vict'] += not score_a
                    players[player_a]['matches'] += 1
                    players[player_b]['matches'] += 1
    sorted_players = sorted(
        players.items(), key=lambda x: x[1]['vict']/x[1]['matches'], reverse=True)
    for player, stats in sorted_players.items():
        victories = stats['vict']
        matches = stats['matches']
        sorted_players[player]['win_ratio'] = victories / matches
    return players


def get_matches_poules_by_link(lien_div: str):
    '''Get matches poules with a link'''
    return connexion_api("xml_result_equ", lien_div)['tour']


def get_match_by_link(lien_match: str):
    '''Get individuals matches with a link'''
    return connexion_api("xml_chp_renc", lien_match).get('partie')


def get_pro_a():
    '''Get the proA team'''
    for team in get_teams_by_club('03350060'):
        if 'FED_PRO A' in team['libdivision']:
            return team['liendivision']
    return ''


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
