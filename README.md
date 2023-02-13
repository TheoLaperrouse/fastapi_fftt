# Fastapi FFTT

## Quick Start
- Renseigner les variables d'environnement suivantes dans un fichier .env à la racine:
```
ID_FFTT=""
KEY_FFTT=""
```

- Lancer le serveur :
```sh
uvicorn src.main:app
```

- Lancez le serveur en mode développement :
```sh
uvicorn src.main:app --reload
```

- Use with docker :
```sh
docker build . -t fastapi_fftt 
```
```sh
docker run fastapi_fftt -p 8000:8000
```
