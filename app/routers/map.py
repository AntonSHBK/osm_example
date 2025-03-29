import logging
from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse

from app.config import settings
from app.services.overpass_client import search_objects
from app.services.osrm_client import get_route
from app.services.map_renderer import render_map

logger = logging.getLogger("api")

router = APIRouter()

@router.get("/map", response_class=HTMLResponse)
async def map_view(
    request: Request,
    bbox: str = Query(
        f"{settings.DEFAULT_BBOX[0]},{settings.DEFAULT_BBOX[1]},{settings.DEFAULT_BBOX[2]},{settings.DEFAULT_BBOX[3]}",
        description="Bounding box: left,top,right,bottom"
    ),
    tag: str = Query(..., description="OSM тег для поиска"),
    from_lat: float = Query(None),
    from_lon: float = Query(None),
    to_lat: float = Query(None),
    to_lon: float = Query(None),
    mode: str = Query("car")
):
    try:
        left, top, right, bottom = map(float, bbox.split(","))
    except ValueError:
        return HTMLResponse(content="Некорректный bbox", status_code=400)

    logger.info("GET /map")
    
    elements = await search_objects(tag, left, top, right, bottom)

    center_lat = (top + bottom) / 2
    center_lon = (left + right) / 2
    route = None

    if from_lat and from_lon and to_lat and to_lon:
        route_data = await get_route((from_lat, from_lon), (to_lat, to_lon), mode=mode)
        if route_data:
            route = route_data["geometry"]
    
    html_map = render_map(elements, route_geojson=route, center=(center_lat, center_lon))
    return HTMLResponse(content=html_map)
