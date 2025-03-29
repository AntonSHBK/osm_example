from fastapi import APIRouter, Query, HTTPException

from app.services.overpass_client import search_objects

router = APIRouter()

@router.get("/search")
async def search(
    bbox: str = Query(..., description="Bounding box: left,top,right,bottom"),
    tag: str = Query(..., description="OSM тег для поиска (например, school, park)")
):
    try:
        left, top, right, bottom = map(float, bbox.split(","))
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат bbox")

    result = await search_objects(tag, left, top, right, bottom)
    if not result:
        raise HTTPException(status_code=404, detail="Объекты не найдены")
    return result
