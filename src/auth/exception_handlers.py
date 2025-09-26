from fastapi import HTTPException, Request, APIRouter, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.auth.exceptions import CustomException

app = FastAPI()

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": [
                {
                    "field": err["loc"][-1],
                    "message": err["msg"]
                } 
                for err in exc.errors()
            ]
        }
    )