import jwt as pyjwt
from src.config import secret_key, algorithm
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_jwt_token(payload:dict):
    """
    Функция создания токена
    """
    # Добавляем срок действия токена
    expire = datetime.now() + timedelta(hours=24)
    payload.update({"exp": expire})
    
    try:
        token = pyjwt.encode(payload, secret_key, algorithm=algorithm)
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token creation error: {str(e)}"
        )

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    """
    Функция для извлечения информации о пользователе из токена. Проверяем токен и извлекаем утверждение о пользователе.
    """
    try:
        payload = pyjwt.decode(token, secret_key, algorithms=[algorithm])  # Декодируем токен с помощью секретного ключа
        return payload.get("sub") 
    except pyjwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail='Сессия закончена')
    except pyjwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')

