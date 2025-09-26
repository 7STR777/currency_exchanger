import psycopg2

from src.config  import dbname, user, password


def user_from_db(username:str):
    """
    Функция сравнения передаваемого логина с юзерами в бд
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT username, password FROM users WHERE username=%s""", (username,))
        user_info_tuple = cur.fetchone()
        user_info = {"username":user_info_tuple[0],
                     "password":user_info_tuple[1]}
        if user_info:
            return user_info
        return None
    except psycopg2.OperationalError as ex:
        # Обработка ошибок подключения (неверный логин, пароль)
        print(f"Не удалось подключиться к базе данных: {ex}")
        return None
    except Exception as e:
        print(f"Произошла другая ошибка{e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            database=dbname,
            user=user,
            password=password
        )
        return conn
    except Exception as ex:
        print(f"[ERROR] Database connection error: {ex}")
        raise

# Подключение к базе данных postgres
def create_database():
    conn = get_db_connection()
    print("Подключение к базе данных установлено")

    conn.autocommit = True

    cur = conn.cursor()
    # Создание новой базы данных
    cur.execute("CREATE DATABASE curexdb")
    conn.commit()
    conn.close()

def insert_into_database():
    conn = get_db_connection()
    print("Подключение к базе данных установлено")
    cur = conn.cursor()

    conn.autocommit = True
    # Создание таблицы users
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(50) NOT NULL
    );""")
    conn.commit()
    conn.close()

def insert_column_into_database():
    conn = get_db_connection()
    print("Подключение к базе данных установлено")
    cur = conn.cursor()

    cur.execute("""ALTER TABLE users ADD COLUMN salt VARCHAR(50)""")
    conn.commit()
    cur.close()
    conn.close()


# except (Exception, psycopg2.Error) as error:
#     print(f"Ошибка при подключении к PostgreSQL: {error}")
# finally:
#     if conn:
#         conn.close()
#         print("Соединение с базой данных закрыто.")