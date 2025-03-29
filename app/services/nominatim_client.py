import httpx
import logging

from app.config import settings

logger = logging.getLogger("app")

async def geocode_address(query: str):
    logger.info(f"Геокодирование: {query}")
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": settings.get_user_agent("nominatim")}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.NOMINATIM_URL}search", params=params, headers=headers
        )
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Ответ от Nominatim (геокодирование): {data}")
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        return None

async def reverse_geocode(lat: float, lon: float):
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1
    }
    headers = {"User-Agent": settings.get_user_agent("nominatim")}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.NOMINATIM_URL}reverse", params=params, headers=headers
        )
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Ответ от Nominatim (обратное геокодирование): {data}")
        if "error" in data:
            return None
        return {
            "lat": lat,
            "lon": lon,
            "display_name": data.get("display_name"),
            "type": data.get("type"),
            "address": data.get("address", {})
        }
