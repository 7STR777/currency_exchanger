import pytest
from unittest.mock import MagicMock

def test_user_registration(client):
        # Тест 1: валидные входные данные
        user_1 = {"username":"user1",
                "password":"testpass"}
        response = client.post("/auth/register", json=user_1)
        assert response.status_code == 200

def test_user_registration_too_short_password(client):
        # Тест 2: короткий пароль(ошибка валидации)
        user_2 = {"username":"user2",
                "password":"test"}
        response = client.post("/auth/register", json=user_2)
        assert response.status_code == 422

def test_user_registration_too_long_password(client):
        # Тест 3: слишком длинный пароль
        user_3 = {"username":"user2",
                "password":"testdasdassadasdsadsadsadsadasdsadsadsadaa"}
        response = client.post("/auth/register", json=user_3)
        assert response.status_code == 422


def test_user_login(client):
        # Тест 4: аутентификация с получением JWT токена
        user_in_1 = {"username":"userfortest", "password":"passfortest"}
        response = client.post("/login", json=user_in_1)
        assert response.status_code == 200

def test_user_login_not_registered(client):
        # Тест 5: аутентификация несуществующего пользователя(ошибка - не зарегестрирован)
        user_in_2 = {"username":"qwerty", "password":"ewqeqweqewq"}
        response = client.post("/login", json=user_in_2)
        assert response.status_code == 401

def test_user_login_bad_password(client):
        # Тест 6: аутентификация пользователя с неправильным паролем
        user_in_3 = {"username":"userfortest", "password":"ewqeqweqewq"}
        response = client.post("/login", json=user_in_3)
        assert response.status_code == 401

def test_exchanger(client):
        pass
        




        
