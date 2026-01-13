from src.queries.orm import AsyncORM
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.auth.schemas import Reviews
from src.auth.security import get_user_from_cookie
from datetime import datetime

review_router = APIRouter()

@review_router.get("/api/reviews")
async def select_article_from_db():
    """
    Возвращает список отзывов в виде JSON, чтобы их можно было
    отрисовать на страницах adminpanel.html и reviews.html через fetch.
    """
    reviews = await AsyncORM.get_review_from_db()
    return [
        {
            "review_id":r.review_id,
            "user_id":r.user_id,
            "username":r.username,
            "rating":r.rating,
            "comment":r.comment,
            "timestamp":r.timestamp
        }
        for r in reviews
    ]

@review_router.post("/api/insert/review")
async def insert_review_into_db(review_data: Reviews, username: str = Depends(get_user_from_cookie)):
    """
    Принимает данные статьи в JSON из формы на reviews.html,
    сохраняет в БД и сообщает об успешном добавлении.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    user_data = await AsyncORM.select_user(
            username
        )


    try:
        await AsyncORM.insert_review_into_db(
            user_id=user_data.user_id,
            username=username,
            rating=review_data.rating,
            comment=review_data.comment,
            timestamp=datetime.now()
        )
        return JSONResponse(content={"message": "Отзыв успешно добавлен"}, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при вставке отзыва: {str(e)}"
        )

@review_router.delete("/api/delete/review/{review_id}")
async def delete_review_id(
    review_id: int,
    username: dict = Depends(get_user_from_cookie)
):
    """
    Удаляет отзыв по ID.
    Доступно только для админов.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    
    user_data = await AsyncORM.select_user(username)
    if user_data.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    try:
        deleted = await AsyncORM.deltete_review(review_id)
        if deleted:
            return JSONResponse(
                content={"message": f"Статья ID {review_id} успешно удалена"},
                status_code=200
            )
        else:
            raise HTTPException(status_code=404, detail="Статья не найдена")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении статьи: {str(e)}"
        )