import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.routers import players, uuid, matches, teams, clubs, padel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_routers(_app):
    '''Initialize routers'''
    routers = [players, uuid, matches, teams, clubs, padel]
    for router in routers:
        _app.include_router(router.router)


app = FastAPI()

init_routers(app)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    '''Redirect to docs on /'''
    return RedirectResponse(url='/docs')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
