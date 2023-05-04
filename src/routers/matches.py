from datetime import datetime
from fastapi import APIRouter
from src.api_connection import connect_api
from src.utils import get_players_by_link
from src.routers.teams import get_pro_a, get_teams_by_club

router = APIRouter(
    prefix="/matches",
    tags=["matches"]
)

@router.get("/proA")
def get_pro_a_stats():
    '''Get pro A statistics'''
    players = {}
    matches = get_matches_poules_by_link(get_pro_a())
    for match in [get_match_info_by_link(m['lien']) for m in matches]:
        if match.get('partie', []) :
            teams = [match['resultat'].get('equa',''),match['resultat'].get('equb','')]
            for individual_match in match.get('partie', []):
                if individual_match and individual_match['ja'] and individual_match['jb']:
                    player_a, player_b = individual_match['ja'], individual_match['jb']
                    score_a = individual_match.get('scorea', -1) == '1'
                    players[player_a] = players.get(player_a, {'vict': 0, 'matches': 0})
                    players[player_a]['vict'] += score_a
                    players[player_b] = players.get(player_b, {'vict': 0, 'matches': 0})
                    players[player_b]['vict'] += not score_a
                    players[player_b]['matches'] += 1
                    players[player_a]['matches'] += 1
                    if 'club' not in players[player_a] :
                        players[player_a]['club'], players[player_b]['club'] = teams
    for stats in players.values():
        stats['win_ratio'] = f'{stats["vict"] / stats["matches"]:.0%}'
    return sorted(players.items(), key=lambda x: x[1]['vict'] / x[1]['matches'], reverse=True)

@router.get("/tftt")
async def get_tftt_matches():
    '''Get all the matches of the TFTT for the actual phase'''
    teams = [team for team in get_teams_by_club("03350060")
                if 'Vétérans' not in team['libdivision']]
    all_matches = [
        {
            **match,
            **(
                get_players_by_link(match['lien'], 'THORIGNE' in match['equa'])
                if isinstance(match['scorea'], str)
                else {}
            ),
            "equa":
                f"{match['equa']} Féminines"
                if 'Féminin' in team.get('libepr', '') and 'THORIGNE' in match['equa']
                else match['equa'],
            "equb":
                f"{match['equb']} Féminines"
                if 'Féminin' in team.get('libepr', '') and 'THORIGNE' in match['equb']
                else match['equb'],
        }
        for team in teams
        for match in get_matches_poules_by_link(team["liendivision"])
        if match is not None
        and match['equa'] is not None
        and match['equb'] is not None
        and ('THORIGNE' in match['equa'] or 'THORIGNE' in match['equb'])
    ]
    return sorted(all_matches, key=lambda d: datetime.strptime(d["dateprevue"], "%d/%m/%Y"))


@router.get("/club/{num_club}")
def get_matches_by_phase(num_club: str):
    '''Get all the matches of a club for the actual phase'''
    teams = get_teams_by_club(num_club)
    all_matches_by_team = [get_matches_poules_by_link(
        team["liendivision"]) for team in teams]
    all_matches = [
        match for matches in all_matches_by_team for match in matches]
    return sorted(all_matches, key=lambda d: datetime.strptime(d["dateprevue"], "%d/%m/%Y"))


@router.get("/{licence}")
def get_match_by_licence(licence: str):
    '''Get last matches by licence'''
    return connect_api("xml_partie", f"numlic={licence}").get('partie')


def get_matches_poules_by_link(lien_div: str):
    '''Get matches poules with a link'''
    return connect_api("xml_result_equ", lien_div).get('tour', [])


def get_match_by_link(lien_match: str):
    '''Get individuals matches with a link'''
    return connect_api("xml_chp_renc", lien_match).get('partie', [])

def get_match_info_by_link(lien_match: str):
    '''Get individuals matches with a link'''
    return connect_api("xml_chp_renc", lien_match)
