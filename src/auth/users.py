from fastapi import HTTPException, status, APIRouter, Form, Depends, Request
from fastapi.security import HTTPBasic
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, Response, JSONResponse
import bcrypt
from auth.schemas import User
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
        raise HTTPException(status_code=400, detail='Пользователь с таким username уже зарегистрирован')
    
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


@userroute.post("/login")
async def login(user_in: Annotated[User, Form()]):
    """
    Этот маршрут проверяет учетные данные пользователя и возвращает JWT токен, если данные правильные.
    """
    user = await AsyncORM.select_user(user_in.username)
    
    if user and bcrypt.checkpw(user_in.password.encode('UTF-8'), user.password.encode('UTF-8')) == True:
        token = create_jwt_token({"sub": user_in.username})
        redirect_response = RedirectResponse(url='/profile', status_code=303)
        redirect_response.set_cookie(
            key="access_token",
            value=token, 
            secure=False,
            httponly=True,
            max_age=1800
        )
        return redirect_response
    else:
        raise HTTPException(status_code=401, detail='Неверный логин или пароль')
        
@userroute.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, username: str = Depends(get_user_from_cookie),):
    user = await AsyncORM.select_user(username)
    return templates.TemplateResponse(
        "profile.html", 
        {
            "request": request,
            "username": user.username,
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
