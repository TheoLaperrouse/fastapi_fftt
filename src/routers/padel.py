from datetime import datetime
from fastapi import APIRouter
import requests
from datetime import datetime, timedelta
import locale
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/padel",
    tags=["padel"]
)


def get_results_string(club_name, court_data):
    results_string = f'<h1>{club_name}</h1>\n'
    for day, days_data in court_data.items():
        if days_data != {}:
            results_string += f"<h2>{day}</h2>\n"
            for hour, durations in sorted(days_data.items()):
                results_string += (
                    f"<p>Heure : {hour}, Durées possibles : {', '.join(sorted(durations))}</p>\n")

    return results_string


clubs = {
    'a126b4d4-a2ee-4f30-bee3-6596368368fb': f'Garden - Parc des Gayeulles : <a href="https://legarden.doinsport.club/select-booking?guid=%22a126b4d4-a2ee-4f30-bee3-6596368368fb%22&from=sport&activitySelectedId=%22ce8c306e-224a-4f24-aa9d-6500580924dc%22&categoryId=%22190e89c2-98a1-4f3b-a23d-df5c921e9324%22">Réservation</a>',
    '348d19e8-95d5-4ffa-880d-8462b832b4ad': f'Soccer Rennais - Route de Lorient : <a href="https://www.soccer-rennais.com/r%C3%A9servations">Réservation</a>',
    '83abc3cd-22ee-4fbd-ac57-5f95b4971d9d': f'Breizh Padel - Bruz : <a href="https://breizhpadel.doinsport.club/select-booking?name=Breizh%20Padel&guid=83abc3cd-22ee-4fbd-ac57-5f95b4971d9d&from=sport">Réservation</a>',
}

params = {
    'from': '8:00:00',
    'to': '23:59:59',
    'activities.id': 'ce8c306e-224a-4f24-aa9d-6500580924dc',
    'bookingType': 'unique',
    'indoor': 'true'
}

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'fr-FR',
}

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

url = 'https://api-v3.doinsport.club/clubs/playgrounds/plannings/'


@router.get("/slots", response_class=HTMLResponse)
def get_padel_slots(days: int = 7):
    '''Get padel over 7 days'''
    res = ''
    start_date = datetime.now()
    for club_id, club_name in clubs.items():
        court_data = {}
        params['club.id'] = club_id
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            current_date_str = current_date.strftime('%Y-%m-%d')
            response = requests.get(
                url + current_date_str, params=params, headers=headers)
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
        res += get_results_string(club_name, court_data)
    return HTMLResponse(content=res)
