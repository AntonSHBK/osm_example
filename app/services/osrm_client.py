import httpx
import logging

from app.config import settings

logger = logging.getLogger("app")


async def get_route(start: tuple[float, float], end: tuple[float, float], mode: str = "car"):
    if mode not in ("car", "foot"):
        raise ValueError("mode must be 'car' or 'foot'")

    logger.info(f"Построение маршрута: {start} → {end} [mode={mode}]")

    profile = "driving" if mode == "car" else "foot"
    coordinates = f"{start[1]},{start[0]};{end[1]},{end[0]}"
    url = f"{settings.OSRM_URL}/route/v1/{profile}/{coordinates}"
    params = {
        "overview": "full",
        "geometries": "geojson"
    }
    headers = {"User-Agent": settings.get_user_agent("osrm")}

    # try:
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("code") != "Ok" or not data.get("routes"):
            logger.warning("Маршрут не найден или ответ невалиден")
            return None

        logger.debug(f"OSRM route: {data}")
        return {
            "distance": data["routes"][0]["distance"],
            "duration": data["routes"][0]["duration"],
            "geometry": data["routes"][0]["geometry"]
        }

    # except httpx.RequestError as e:
    #     logger.error(f"Ошибка запроса к OSRM: {e}")
    #     return None
