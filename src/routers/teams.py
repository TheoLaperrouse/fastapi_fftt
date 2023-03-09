import re
from fastapi import APIRouter
from src.connexion_api import connexion_api
from src.utils import get_actual_phase

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)


def get_pro_a():
    '''Get the proA team'''
    for team in get_all_teams_by_club('03350060'):
        if 'FED_PRO A' in team['libdivision']:
            return team['liendivision']
    return None


@router.get("/all/{num_club}")
def get_all_teams_by_club(num_club: str):
    '''Get teams by num club'''
    return connexion_api("xml_equipe", f"numclu={num_club}").get("equipe")


@router.get("/{num_club}")
def get_teams_by_club(num_club: str):
    '''Get teams by club num for the actual phase'''
    phase = get_actual_phase()
    teams = connexion_api("xml_equipe", f"numclu={num_club}").get("equipe")
    regex_phase = re.compile(f"Phase {phase}|Ph{phase}|Ph {phase}")
    return [team for team in teams if regex_phase.findall(team['libdivision'])]
