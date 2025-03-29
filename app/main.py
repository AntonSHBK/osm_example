from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import geocode, map_interactive, search, route, map, app_ui, map_interactive

app = FastAPI(title="OSM Geo Service")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(geocode.router)
app.include_router(search.router)
app.include_router(route.router)
app.include_router(map.router)
app.include_router(app_ui.router)
app.include_router(map_interactive.router)
