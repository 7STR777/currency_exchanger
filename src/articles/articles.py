from src.queries.orm import AsyncORM
from fastapi import APIRouter

article_router = APIRouter()

@article_router.get("/api/articles")
async def select_article_from_db():
    arcticles = await AsyncORM.get_article_from_db()
    return arcticles