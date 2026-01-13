from fastapi import HTTPException, status, APIRouter, Form, Depends, Request
from fastapi.security import HTTPBasic
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, Response, JSONResponse
import bcrypt
from auth.schemas import User, UserLogin
from src.auth.security import create_jwt_token, get_user_from_header, get_user_from_cookie
from src.queries.orm import AsyncORM
from typing import Annotated
from fastapi.templating import Jinja2Templates


userroute = APIRouter()
security = HTTPBasic()
templates = Jinja2Templates(directory="src/frontend/templates")

@userroute.post("/registration")
async def register(us: Annotated[User, Form()]
):
    """
    Этот маршрут регистрирует пользователя в базе данных.
    INSERT INTO users (username, password, email) VALUES (%s, %s, %s)
    """
    existing_user = await AsyncORM.select_user(us.username)
    if existing_user:
        return HTTPException(
            status_code=400,                   
            detail='Пользователь с таким username уже зарегистрирован', 
            headers={
                "username":existing_user.username
            }
            )
    
    hashed_password = bcrypt.hashpw(us.password.encode('UTF-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    try:
        await AsyncORM.insert_user(us.username, hashed_password, us.email)
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        print(f"Произошла ошибка при вставке данных: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка при регистрации пользователя: {str(e)}"
        )


@userroute.get("/check-username")
async def check_username(username: str):
    """
    Вспомогательный маршрут для проверки существования пользователя.
    """
    existing_user = await AsyncORM.select_user(username)
    return {"exists": bool(existing_user)}


@userroute.post("/login")
async def login(user_in: Annotated[UserLogin, Form()], response: Response):
    """
    Этот маршрут проверяет учетные данные пользователя и возвращает JWT токен, если данные правильные.
    """
    user = await AsyncORM.select_user(user_in.username)
    
    if user and bcrypt.checkpw(user_in.password.encode('UTF-8'), user.password.encode('UTF-8')):
        token = create_jwt_token({"sub": user_in.username})
        
        response.set_cookie(
            key="access_token",
            value=token, 
            httponly=True,
            secure=True,
            samesite='strict',
            max_age=1800
        )
        return {
            "username": user.username,
            "role": user.role,
            "email": user.email,
            "redirect_url": "/profile"
        }
    
    return JSONResponse(
        status_code=401,
        content={"detail": "Неверный логин или пароль"}
    )


        
@userroute.get("/editarticles", response_class=HTMLResponse)
async def edit_articles(request: Request, username: str = Depends(get_user_from_cookie)):
    user = await AsyncORM.select_user(username)
    if username != "admin":
        return RedirectResponse(url='/profile', status_code=303)
    return templates.TemplateResponse(
        "editarticles.html",
        {
            "request":request,
            "username":user.username,
            "role":user.role,
            "email":user.email
        }
    )

@userroute.get("/editreviews", response_class=HTMLResponse)
async def edit_reviews(request: Request, username: str = Depends(get_user_from_cookie)):
    user = await AsyncORM.select_user(username)
    if username != "admin":
        return RedirectResponse(url='/profile', status_code=303)
    return templates.TemplateResponse(
        "editreviews.html",
        {
            "request":request,
            "username":user.username,
            "role":user.role,
            "email":user.email
        }
    )

@userroute.get("/editbanners", response_class=HTMLResponse)
async def edit_banners(request: Request, username: str = Depends(get_user_from_cookie)):
    user = await AsyncORM.select_user(username)
    if username != "admin":
        return RedirectResponse(url='/profile', status_code=303)
    return templates.TemplateResponse(
        "editbanners.html",
        {
            "request":request,
            "username":user.username,
            "role":user.role,
            "email":user.email
        }
    )

@userroute.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, username: str = Depends(get_user_from_cookie)):
    user = await AsyncORM.select_user(username)
    
    if user.role == "admin":
        return templates.TemplateResponse(
            "adminprofile.html",
            {"request": request, "username": user.username, "role": user.role, "email": user.email}
        )
    
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "username": user.username, "role": user.role, "email": user.email}
    )

@userroute.get("/articles", response_class=HTMLResponse)
async def articles_page(request: Request, username: str = Depends(get_user_from_cookie)):
    user = await AsyncORM.select_user(username)
    return templates.TemplateResponse(
        "articles.html",
        {
            "request":request,
            "username":user.username,
            "email":user.email
        }
    )

@userroute.get("/reviews", response_class=HTMLResponse)
async def reviews_page(request: Request, username: str = Depends(get_user_from_cookie)):
    user = await AsyncORM.select_user(username)
    return templates.TemplateResponse(
        "reviews.html",
        {
            "request":request,
            "username":user.username,
            "email":user.email
        }
    )

@userroute.post("/logout")
async def logout():
    response = JSONResponse({
        "message": "Успешный выход из системы", 
        "redirect_url": "/login"
    })
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False
    )
    return response
