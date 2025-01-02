import locale
from datetime import datetime, timedelta
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import requests
import uuid
import requests
import random
import string
from requests_toolbelt import MultipartEncoder

router = APIRouter(
    prefix="/padel",
    tags=["padel"]
)

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


def parse_date(date_str):
    try:
        datetime_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            datetime_object = datetime.strptime(
                date_str, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError as e:
            print(f"Erreur de format de date : {e}")
            return None
    return datetime_object


def format_name_club(name, link):
    '''Format Name club to html'''
    return f'{name} : <a href="{link}">Réservation</a>'


CLUBS = {
    'a126b4d4-a2ee-4f30-bee3-6596368368fb': format_name_club('Garden - Parc des Gayeulles', 'https://legarden.doinsport.club/select-booking?activitySelectedId=%22ce8c306e-224a-4f24-aa9d-6500580924dc%22'),
    '348d19e8-95d5-4ffa-880d-8462b832b4ad': format_name_club('Soccer Rennais - Route de Lorient', 'https://www.soccer-rennais.com/r%C3%A9servations'),
    '83abc3cd-22ee-4fbd-ac57-5f95b4971d9d': format_name_club('Breizh Padel - Bruz', 'https://breizhpadel.doinsport.club/select-booking?name=Breizh%20Padel&guid=83abc3cd-22ee-4fbd-ac57-5f95b4971d9d&from=sport')
}
URBAN_CLUBS = {
    '15': format_name_club('Urban Padel - Rennes / Vern', 'https://myurban.fr/padel/reserver?centerId=15&activity=7'),
    '19': format_name_club('Urban Padel - Cap Malo', 'https://myurban.fr/padel/reserver?centerId=19&activity=7')
}


def get_html_result(club_name, court_data):
    '''Format result object to html'''
    results_string = f'<h1>{club_name}</h1>\n'
    for day, days_data in court_data.items():
        if days_data != {}:
            results_string += f"<h2>{day}</h2>\n"
            for hour, durations in sorted(days_data.items()):
                results_string += (
                    f"<p>Heure : {hour}, Durées possibles : {', '.join(sorted(durations))}</p>\n")

    return results_string


def format_doin_sport(club_id, days):
    '''Format slots of DoInSport API'''
    start_date = datetime.now()
    url = 'https://api-v3.doinsport.club/clubs/playgrounds/plannings/'
    params = {
        'from': '8:00:00',
        'to': '23:59:59',
        'activities.id': 'ce8c306e-224a-4f24-aa9d-6500580924dc',
        'bookingType': 'unique',
        'indoor': 'true'
    }
    court_data = {}
    params['club.id'] = club_id
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        current_date_str = current_date.strftime('%Y-%m-%d')
        try:
            response = requests.get(
                url + current_date_str,
                params=params,
                headers={
                    'Accept': 'application/json',
                    'Accept-Language': 'fr-FR',
                    'If-None-Match': str(uuid.uuid4()).replace("-", "")
                },
                timeout=30
            )
            response.raise_for_status()
            for court in response.json():
                day = current_date.strftime('%A %d %B').capitalize()
                if day not in court_data:
                    court_data[day] = {}
                for activity in court['activities']:
                    for slot in activity['slots']:
                        for price in slot['prices']:
                            if price.get('bookable', False):
                                hour = slot['startAt']
                                duration = f'{int(price["duration"] / 60)} min'
                                court_data[day].setdefault(
                                    hour, set()).add(duration)
        except Exception as e:
            print(
                f"Erreur lors de l'appel DoInSport pour le club {club_id} : {e}")
    return court_data


def format_urban_soccer(club_id, days):
    '''Format slots of Urban Padel'''
    start_date = datetime.now()
    court_data = {}
    for day in range(days):
        url = "https://myurban.fr/api/read/reservation/availabilities/search"
        current_date = start_date + timedelta(days=day)
        current_date_str = current_date.strftime('%Y-%m-%d')
        fields = {
            "categories": "[7]",
            "centerId": club_id,
            "periodStart": current_date_str,
        }

        boundary = '----WebKitFormBoundary' + \
            ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        data = MultipartEncoder(fields=fields, boundary=boundary)

        headers = {
            "accept": "application/json",
            "activity": "2",
            "content-type": data.content_type
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            json = response.json()

            for slot in json['data'][1]:
                day = current_date.strftime('%A %d %B').capitalize()
                if day not in court_data:
                    court_data[day] = {}
                datetime_object = parse_date(slot['start'])
                hour = datetime_object.time().strftime("%H:%M")
                duration = f"{slot['duration']} min"
                court_data[day].setdefault(hour, set()).add(duration)
        except Exception as e:
            print(
                f"Erreur lors de l'appel Urban Padel pour le club {club_id} : {e}")
    return court_data


@router.get("/slots", response_class=HTMLResponse)
def get_padel_slots(days: int = 3):
    '''Get padel over n days'''
    res = ''

    for club_id, club_name in CLUBS.items():
        court_data = format_doin_sport(club_id, days)
        res += get_html_result(club_name, court_data)
    for club_id, club_name in URBAN_CLUBS.items():
        court_data = format_urban_soccer(club_id, days)
        res += get_html_result(club_name, court_data)
    return HTMLResponse(content=f'''<html>
                                    <head>
                                        <style>
                                            body {{
                                                font-family: Arial, sans-serif;
                                                background-color: #f4f4f4;
                                                margin: 20px;
                                            }}
                                            h1 {{
                                                color: #333;
                                            }}
                                            h2 {{
                                                color: #555;
                                            }}
                                            p {{
                                                color: #777;
                                            }}
                                        </style>
                                    </head>
                                        <body>{res}</body>
                                    </html>
                                    ''')
