from fastapi import APIRouter
from src.api_connection import connect_api

router = APIRouter(
    prefix="/clubs",
    tags=["clubs"]
)


@router.get("/dep/{department}")
def get_club_by_department(department: str):
    '''Get clubs by department'''
    return connect_api("xml_club_dep2", f"dep={department}")["club"]


@router.get("/id/{clubId}")
def get_club_by_id(clubId: str):
    '''Get club by id'''
    return connect_api("xml_club_detail", f"club={clubId}")["club"]
