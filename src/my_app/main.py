import os
import sys
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
REPO_ROOT = os.path.dirname(SRC_DIR)
for path_candidate in (REPO_ROOT, SRC_DIR):
    if path_candidate and path_candidate not in sys.path:
        sys.path.insert(0, path_candidate)


from src.auth.users import userroute
from src.auth.currency import currencyroute
from src.auth.exception_handlers import validation_exception_handler, custom_exception_handler
from src.auth.exceptions import CustomException



app = FastAPI()
app.include_router(userroute)
app.include_router(currencyroute)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
def index():
    return {"message":"Main page of currency exchanger"}