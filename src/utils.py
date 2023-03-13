from datetime import datetime
from src.api_connection import connect_api


def get_actual_phase():
    '''Get the actual phase (1 or 2)'''
    return 1 if datetime.now().month > 8 else 2


def get_players_by_link(lien_match, is_equ_a):
    '''Get players of a match by link'''
    games = connect_api("xml_chp_renc", lien_match)
    joueurs_a = []
    joueurs_b = []
    if games["joueur"] is not None:
        for joueur in games["joueur"]:
            is_sorted = is_equ_a != ('THORIGNE' in games["resultat"]["equa"])
            joueurs_a.append(joueur["xja"] if not is_sorted else joueur["xjb"])
            joueurs_b.append(joueur["xjb"] if not is_sorted else joueur["xja"])
        return {"joueursA": joueurs_a, "joueursB": joueurs_b}
    return {}
