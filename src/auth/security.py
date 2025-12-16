import jwt as pyjwt
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from fastapi.requests import Request
from fastapi import HTTPException, status, Depends, Cookie
from datetime import datetime, timedelta
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
security = HTTPBearer(auto_error=False)

def create_jwt_token(payload:dict):
    """
    Функция создания токена
    """
    expire = datetime.now() + timedelta(hours=24)
    payload.update({"exp": expire})
    
    try:
        token = pyjwt.encode(payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token creation error: {str(e)}"
        )

def get_user_from_header(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Зависимость для получения пользователя из cookie access_token.
    """
    if not credentials:
        raise HTTPException(status_code=401, detail='Токен не предоставлен')
    try:
        payload = pyjwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        return username
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Сессия закончена')
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')
    
def get_user_from_cookie(request: Request):
    """
    Зависимость для получения пользователя из cookie access_token. Возвращает username пользователя.
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail='Токен не предоставлен')
    try:
        payload = pyjwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        return username
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Сессия закончена')
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')