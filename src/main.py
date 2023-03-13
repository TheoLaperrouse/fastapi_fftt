import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_utils.timing import add_timing_middleware
from src.routers import players, uuid, matches, teams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_routers(_app):
    '''Initialize routers'''
    routers = [players, uuid, matches, teams]
    for router in routers:
        _app.include_router(router.router)


app = FastAPI()
init_routers(app)
add_timing_middleware(app, record=logger.info, prefix="app", exclude="untimed")

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    '''Redirect to docs on /'''
    return RedirectResponse(url='/docs')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
