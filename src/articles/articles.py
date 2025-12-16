from src.queries.orm import AsyncORM
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from src.auth.schemas import Article
from src.auth.security import get_user_from_cookie


article_router = APIRouter()
templates = Jinja2Templates(directory="src/frontend/templates")


@article_router.get("/api/articles")
async def select_article_from_db():
    """
    Возвращает список статей в виде JSON, чтобы их можно было
    отрисовать на страницах adminpanel.html и articles.html через fetch.
    """
    articles = await AsyncORM.get_article_from_db()
    return [
        {
            "article_id": a.article_id,
            "title": a.title,
            "intro_text": a.intro_text,
            "full_text": a.full_text,
            "codeimg": a.codeimg,
        }
        for a in articles
    ]


@article_router.post("/api/insert/article")
async def insert_article_into_db(art: Article, username: str = Depends(get_user_from_cookie)):
    """
    Принимает данные статьи в JSON из формы на adminpanel.html,
    сохраняет в БД и сообщает об успешном добавлении.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")

    try:
        await AsyncORM.insert_article_into_db(
            art.title,
            art.intro_text,
            art.full_text,
            art.codeimg,
        )
        return JSONResponse(content={"message": "Статья успешно добавлена"}, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при вставке статьи: {str(e)}"
        )


@article_router.get("/article/{article_id}", response_class=HTMLResponse)
async def article_page(
    request: Request,
    article_id: int,
    username: str = Depends(get_user_from_cookie),
):
    """
    HTML‑страница отдельной статьи по её ID.
    Показывает full_text и codeimg из базы данных.
    """
    # Получаем пользователя для шапки сайта
    user = await AsyncORM.select_user(username)

    # Получаем статью
    article = await AsyncORM.get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    return templates.TemplateResponse(
        "article.html",
        {
            "request": request,
            "username": user.username if user else "",
            "email": user.email if user else "",
            "article": article,
        },
    )

@article_router.delete("/api/delete/article/{article_id}")
async def delete_article_from_db(
    article_id: int,
    username: dict = Depends(get_user_from_cookie)
):
    """
    Удаляет статью по ID.
    Доступно только для админов.
    """
    if not username:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    
    user_data = await AsyncORM.select_user(username)
    if user_data.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    try:
        deleted = await AsyncORM.delete_article(article_id)
        if deleted:
            return JSONResponse(
                content={"message": f"Статья ID {article_id} успешно удалена"},
                status_code=200
            )
        else:
            raise HTTPException(status_code=404, detail="Статья не найдена")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении статьи: {str(e)}"
        )