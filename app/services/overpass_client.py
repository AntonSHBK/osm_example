import logging
import httpx
from app.config import settings

logger = logging.getLogger("app")

def build_overpass_query(tag: str, left: float, top: float, right: float, bottom: float) -> str:
    return f"""
    [out:json][timeout:25];
    (
      node["amenity"="{tag}"]({bottom},{left},{top},{right});
      way["amenity"="{tag}"]({bottom},{left},{top},{right});
      relation["amenity"="{tag}"]({bottom},{left},{top},{right});
    );
    out center;
    """

async def search_objects(tag: str, left: float, top: float, right: float, bottom: float):
    logger.info(f"Поиск объектов '{tag}' в bbox ({left},{top},{right},{bottom})")

    query = build_overpass_query(tag, left, top, right, bottom)

    headers = {"User-Agent": settings.get_user_agent("overpass")}
    async with httpx.AsyncClient() as client:
        logger.info(f"Overpass QL:\n{query}")
        response = await client.post(settings.OVERPASS_URL, data=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("elements", [])
