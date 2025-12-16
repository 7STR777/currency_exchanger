from src.queries.orm import AsyncORM
from fastapi import APIRouter, Depends, HTTPException
from src.auth.schemas import Banner
from src.auth.security import get_user_from_cookie
from fastapi.responses import JSONResponse

banner_router = APIRouter()

@banner_router.get("/api/banners")
async def get_active_banners():
    banners = await AsyncORM.select_banners()
    return banners

@banner_router.post("/api/insert/banner")
async def insert_banner_into_db(banner: Banner, username: str = Depends(get_user_from_cookie)):
    """
    Принимает данные баннера в JSON из формы и,
    сохраняет в БД и сообщает об успешном добавлении.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")

    try:
        await AsyncORM.insert_banner_into_db(
            banner.code
        )
        return JSONResponse(content={"message": "Баннер успешно добавлена"}, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при вставке банера: {str(e)}"
        )
    
@banner_router.delete("/api/delete/banner/{banner_id}")
async def delete_banner(banner_id: int, username: str = Depends(get_user_from_cookie)):
    """
    Удаляет баннер по ID.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")

    try:
        await AsyncORM.delete_banner(banner_id)
        return JSONResponse(content={"message": "Баннер успешно удален"}, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении баннера: {str(e)}"
        )