from fastapi import FastAPI
from src.connexion_API import connexion_api
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/players/{licence}")
def getPlayerByLicence(licence: int):
    res = connexion_api("xml_joueur", f"licence={licence}")
    return res


@app.get("/players/club/{numClub}")
def getPlayersByClub(numClub: str):
    res = connexion_api("xml_liste_joueur", f"club={numClub}")
    return res


@app.get("/matches/{licence}")
def getMatchesByLicence(licence: str):
    res = connexion_api("xml_liste_joueur", f"licence={licence}")
    return res


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
