from fastapi import APIRouter, Query, HTTPException

from app.services.osrm_client import get_route

router = APIRouter()

@router.get("/route")
async def route(
    from_lat: float = Query(..., description="Широта точки отправления"),
    from_lon: float = Query(..., description="Долгота точки отправления"),
    to_lat: float = Query(..., description="Широта точки назначения"),
    to_lon: float = Query(..., description="Долгота точки назначения"),
    mode: str = Query("car", description="Тип маршрута: car или foot")
):
    try:
        result = await get_route(
            start=(from_lat, from_lon),
            end=(to_lat, to_lon),
            mode=mode
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not result:
        raise HTTPException(status_code=404, detail="Маршрут не найден")

    return result
