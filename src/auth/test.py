# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from src.auth.schemas import User
# from src.auth.security import create_jwt_token, get_user_from_token
# from src.database import get_db_connection, user_from_db
# from src.config import secret_key, algorithm
# import jwt as pyjwt
import hashlib
import os
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# DBNAME = "currencyexchange"
# USER = "postgres"
# PASSWORD = "igor2003"
# import jwt  # тут используем библиотеку PyJWT

# # Секретный ключ для подписи и верификации токенов JWT
# SECRET_KEY = "mysecretkey"  # в реальной практике используем что-нибудь вроде команды Bash (Linux) 'openssl rand -hex 32' и храним очень защищённо
# ALGORITHM = "HS256"  # плюс в реальной жизни устанавливаем "время жизни" токена

# # Пример информации из БД
# USERS_DATA = [
#     {"username": "admin", "password": "adminpass"}
# ]  # в реальной БД храним только ХЭШИ паролей (например, с помощью библиотеки 'passlib') + соль (известная только нам добавка к паролю)

# # Функция для создания JWT токена

# def user_from_db(username:str):
#     try:
#         conn = get_db_connection()
#         cur = conn.cursor()
#         cur.execute("""SELECT username, password FROM users WHERE username=%s""", (username,))
#         user_info_tuple = cur.fetchone()
#         user_info = {"username":user_info_tuple[0],
#                      "password":user_info_tuple[1]}
#         if user_info:
#             return user_info
#         return None
#     except Exception as ex:
#         print(f"Error: {ex}")
#         return {"message":"Произошла ошибка"}
#     finally:
#         if cur:
#             cur.close()
#         if conn:
#             conn.close()

# # try:
# #     conn = get_db_connection()
# #     cur = conn.cursor()
# #     cur.execute("""INSERT INTO users (username, password) 
# #         VALUES (%s, %s)""", (us.username, us.password))
# #     return {"message":"Пользователь успешно зарегестрирован!"}
# # except Exception as ex:
# #     print(f"Error: {ex}")
# #     return {"message":"Произошла ошибка"}

# # def user_from_db(username:str):
# #     try:
# #         conn = psycopg2.connect(
# #         database=DBNAME,
# #         user=USER,
# #         password=PASSWORD
# #         )
# #         cur = conn.cursor()
# #         cur.execute("""SELECT username, password FROM users WHERE username=%s""", (username,))
# #         user = cur.fetchone()
# #         if user:
# #             return user
# #         return None
# #     except Exception as ex:
# #         print(f"Error: {ex}")
# #         return {"message":"Произошла ошибка"}
# #     finally:
# #         if cur:
# #             cur.close()
# #         if conn:
# #             conn.close()
# # test = ("123", "321")
# # print(jwt.__file__)
# # print(user_from_db("user1"))

# def get_user_from_token(token):
#     """
#     Функция для извлечения информации о пользователе из токена. Проверяем токен и извлекаем утверждение о пользователе.
#     """
#     try:
#         payload = pyjwt.decode(token, secret_key, algorithms=[algorithm])  # Декодируем токен с помощью секретного ключа
#         return payload.get("sub") 
#     except pyjwt.ExpiredSignatureError:
#         pass  
#     except pyjwt.InvalidTokenError:
#         pass 

# q = {'success': True,
#     'query': {'from': 'RUB', 'to': 'AED', 'amount': 100000},
#     'info': {'timestamp': 1756919046, 'quote': 0.045414},
#     'result': 4541.4
#     }
# print(q["result"])
my_dict = {'username':"1231231", "password":"testpass"}
print(my_dict.get("password"))
print(type(my_dict.get("password")))