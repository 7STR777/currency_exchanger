import os
from dotenv import load_dotenv

load_dotenv()
dbname = os.getenv("DBNAME")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
