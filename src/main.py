from fastapi import FastAPI
from src.connexion_API import connexion_api
import uvicorn

app = FastAPI()


@app.get("/players/{licence}")
def getPlayerByLicence(licence: str):
    return connexion_api("xml_joueur", f"licence={licence}")['joueur']


@app.get("/players/club/{numClub}")
def getPlayersByClub(numClub: str):
    return connexion_api("xml_liste_joueur", f"club={numClub}")['joueur']


@app.get("/matches/{licence}")
def getMatchesByLicence(licence: str):
    return connexion_api("xml_partie", f"numlic={licence}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
