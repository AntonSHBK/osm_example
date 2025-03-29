from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services.osrm_client import get_route
from app.services.nominatim_client import geocode_address

router = APIRouter()


@router.get("/map/interactive-data")
async def interactive_route_data(
    from_lat: float = Query(...),
    from_lon: float = Query(...),
    to_lat: float = Query(...),
    to_lon: float = Query(...),
    mode: str = Query("car")
):
    """
    Построение маршрута по координатам (используется при кликах по карте)
    """
    route_data = await get_route(
        (from_lat, from_lon),
        (to_lat, to_lon),
        mode=mode
    )

    if not route_data:
        return JSONResponse(content={"error": "Route not found"}, status_code=404)

    return {
        "type": "Feature",
        "geometry": route_data["geometry"]
    }


@router.get("/map/from-names")
async def route_from_names(
    from_: str = Query(..., alias="from"),
    to: str = Query(...),
    mode: str = Query("car")
):
    """
    Построение маршрута по названиям (через геокодирование)
    """
    from_coords = await geocode_address(from_)
    to_coords = await geocode_address(to)

    if not from_coords or not to_coords:
        return JSONResponse(
            content={"error": "One or both locations not found"},
            status_code=404
        )

    route_data = await get_route(
        (float(from_coords["lat"]), float(from_coords["lon"])),
        (float(to_coords["lat"]), float(to_coords["lon"])),
        mode=mode
    )

    if not route_data:
        return JSONResponse(
            content={"error": "Route not found"},
            status_code=404
        )

    return {
        "type": "Feature",
        "geometry": route_data["geometry"]
    }
