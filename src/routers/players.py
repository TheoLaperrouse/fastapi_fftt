from fastapi import APIRouter
from src.api_connection import connect_api

router = APIRouter(
    prefix="/players",
    tags=["players"]
)


@router.get("/name/{last_name}_{first_name}")
def get_player_by_name(last_name: str, first_name: str):
    '''Get player by name'''
    return connect_api("xml_liste_joueur_o", f"nom={last_name}&prenom={first_name}").get('joueur')


@router.get("/club/{num_club}")
def get_players_by_club(num_club: str):
    '''Get players by club num'''
    return connect_api("xml_liste_joueur", f"club={num_club}").get('joueur')


@router.get("/{licence}")
def get_player_by_licence(licence: str):
    '''Get player by licence'''
    return connect_api("xml_joueur", f"licence={licence}").get('joueur')
