import requests
import csv

departements = [f'{i:02}' for i in range(1,96)] 

clubsInfos = []
with open('contacts_ping.csv', newline='', mode='a') as csv_file:
    csv_writer = csv.writer(csv_file)
    for dep in departements:
        res = requests.get(f"http://127.0.0.1:8000/clubs/dep/{dep}", timeout=60)
        for club in res.json():
            request = requests.get(f"http://127.0.0.1:8000/clubs/id/{club['numero']}", timeout=60)
            clubInfos = request.json()
            if clubInfos:
                csv_writer.writerow([
                    "Club",
                    clubInfos.get("nom",""),
                    "",
                    clubInfos.get("nomcor",""),
                    clubInfos.get("prenomcor",""),
                    clubInfos.get("telcor",""),
                    clubInfos.get("mailcor",""),
                    clubInfos.get("nomsalle",""),
                    clubInfos.get("adressesalle1",""),
                    clubInfos.get("codepsalle",""),
                    clubInfos.get("villesalle",""),
              ])
            
        