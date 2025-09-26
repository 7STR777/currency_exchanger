from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from src.auth.users import userroute
from src.auth.currency import currencyroute
from src.auth.exception_handlers import validation_exception_handler, custom_exception_handler
from src.auth.exceptions import CustomException, CustomValidationException
from fastapi.responses import FileResponse


app = FastAPI()
app.include_router(userroute)
app.include_router(currencyroute)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/")
def index():
    return {"message":"Main page of currency exchanger"}

