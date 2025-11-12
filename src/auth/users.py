from fastapi import HTTPException, status, APIRouter
from fastapi.security import HTTPBasic
import bcrypt
from auth.schemas import User
from src.auth.security import create_jwt_token
from src.queries.orm import AsyncORM


userroute = APIRouter()
security = HTTPBasic()


@userroute.post("/auth/register")
async def register(us: User):
    """
    Этот маршрут регистрирует пользователя в базе данных.
    INSERT INTO users (username, password) VALUES (%s, %s)
    """
    if us.password is None:
        raise HTTPException(status_code=400, detail='Необходимо ввести пароль')
    if us.username is None:
        raise HTTPException(status_code=400, detail='Необходимо ввести логин')
    hashed_password = bcrypt.hashpw(us.password.encode('UTF-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    try:
        await AsyncORM.insert_user(us.username, hashed_password)
        return {"message": "Пользователь успешно зарегистрирован", "username": us.username}
    except Exception as e:
        print(f"Произошла ошибка при вставке данных: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Ошибка при регистрации пользователя: {str(e)}"
        )


@userroute.post("/login")
async def login(user_in: User):
    """
    Этот маршрут проверяет учетные данные пользователя и возвращает JWT токен, если данные правильные.
    """
    user = await AsyncORM.select_user(user_in.username)
    print(user)
    if user and bcrypt.checkpw(user_in.password.encode('UTF-8'), user.password.encode('UTF-8')) == True:
        token = create_jwt_token({"sub": user_in.username})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail='Неверный логин или пароль')