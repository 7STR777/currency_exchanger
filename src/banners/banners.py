from src.queries.orm import AsyncORM
from fastapi import APIRouter, Depends, HTTPException

banner_router = APIRouter()

@banner_router.get("/api/banners")
async def get_active_banners():
    banners = await AsyncORM.select_banners()
    return banners