from fastapi import HTTPException, status, APIRouter
from fastapi.security import HTTPBasic

import bcrypt

from src.auth.schemas import User
from src.auth.security import create_jwt_token
from src.database import get_db_connection, user_from_db


userroute = APIRouter()
security = HTTPBasic()

@userroute.post("/auth/register")
async def register(us: User):
    """
    Этот маршрут регистрирует пользователя в базе данных.
    """
    if us.password is None:
        raise HTTPException(status_code=400, detail='Необходимо ввести пароль')
    if us.username is None:
        raise HTTPException(status_code=400, detail='Необходимо ввести логин')
    hashed_password = bcrypt.hashpw(us.password.encode('UTF-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""INSERT INTO users (username, password) 
            VALUES (%s, %s)""", (us.username, hashed_password))
        conn.commit()
        return {"message":"Вы успешно зарегестрированы!"}
    except Exception as ex:
        print(f"Error: {ex}")
        return {"message": "Произошла ошибка"}
    finally:
        if cur:
            cur.close()


@userroute.post("/login")
async def login(user_in: User):
    """
    Этот маршрут проверяет учетные данные пользователя и возвращает JWT токен, если данные правильные.
    """
    user = user_from_db(user_in.username)
    if user and bcrypt.checkpw(user_in.password.encode('UTF-8'), user.get('password').encode('utf-8')):
        token = create_jwt_token({"sub": user_in.username})
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
