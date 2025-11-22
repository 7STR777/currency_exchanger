from fastapi import Depends, APIRouter, HTTPException, status
from auth.security import get_user_from_header, get_user_from_cookie
import requests
from config import settings

currencyroute = APIRouter()


@currencyroute.get("/api/convert")
async def currency_exchange(convert_from: str, convert_to: str, convert_amount: str, current_user: str = Depends(get_user_from_cookie)):
    """
    Этот маршрут защищен и требует токен. Выдает свежие обменные курсы для различных валют.
    """
    headers = {"apikey":settings.API_KEY}
    URL = f"{settings.BASE_URL}convert?to={convert_to}&from={convert_from}&amount={convert_amount}"
    response = requests.request("GET", URL, headers=headers)

    if response.status_code == 200:
        result = response.json() 
        return {"Convertation result":{"Convert_from":convert_from,
                "Amount":int(convert_amount),
                "Convert_to":convert_to,
                "Converted_amount":result["result"]}}
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail='Вы не авторизованы!')

@currencyroute.get("/api/rates")
async def currency_list(current_user: str = Depends(get_user_from_cookie)):
    """
    Этот маршрут защищен и требует токен. Выдает список доступных валют к обмену.
    """
    headers = {"apikey":settings.API_KEY}
    URL = 'https://api.apilayer.com/currency_data/list'
    response = requests.request("GET", URL, headers=headers)
    result_list = response.json()
    return result_list
    