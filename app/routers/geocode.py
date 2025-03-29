import logging
from fastapi import APIRouter, Query, HTTPException

from app.services.nominatim_client import geocode_address, reverse_geocode

logger = logging.getLogger("api")

router = APIRouter()

@router.get("/geocode")
async def geocode(q: str = Query(..., description="Адрес или запрос для геокодирования")):
    logger.info(f"GET /geocode?q={q}")
    coords = await geocode_address(q)
    if not coords:
        raise HTTPException(status_code=404, detail="Адрес не найден")
    return {"query": q, "lat": coords[0], "lon": coords[1]}

@router.get("/reverse-geocode")
async def reverse(
    lat: float = Query(..., description="Широта"),
    lon: float = Query(..., description="Долгота")
):
    logger.info(f"GET /reverse-geocode?lat={lat}&lon={lon}")
    result = await reverse_geocode(lat, lon)
    if not result:
        raise HTTPException(status_code=404, detail="Объект не найден")
    return result
