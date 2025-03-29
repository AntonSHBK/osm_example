import logging

import folium
from folium.plugins import MarkerCluster

from app.config import settings

logger = logging.getLogger("app")

def render_map(elements: list, route_geojson: dict | None = None, center: tuple = None, zoom_start: int = 13) -> str:
    logger.info("Генерация карты Folium")
    
    center = center or settings.DEFAULT_CENTER
    
    fmap = folium.Map(location=center, zoom_start=zoom_start)
    marker_cluster = MarkerCluster().add_to(fmap)

    # Добавим найденные объекты
    for el in elements:
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        name = el.get("tags", {}).get("name", "Без названия")
        folium.Marker(
            location=(lat, lon),
            popup=name,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

    # Добавим маршрут
    if route_geojson:
        folium.GeoJson(
            data=route_geojson,
            name="Маршрут",
            style_function=lambda x: {"color": "red", "weight": 5}
        ).add_to(fmap)

    return fmap._repr_html_()
