import os
import sys
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
REPO_ROOT = os.path.dirname(SRC_DIR)
for path_candidate in (REPO_ROOT, SRC_DIR):
    if path_candidate and path_candidate not in sys.path:
        sys.path.insert(0, path_candidate)

from src.auth.users import userroute
from src.auth.currency import currencyroute
from src.banners.banners import banner_router
from src.articles.articles import article_router
from src.auth.exception_handlers import validation_exception_handler, custom_exception_handler
from src.auth.exceptions import CustomException
from src.auth.security import get_user_from_header


app = FastAPI()
app.include_router(userroute)
app.include_router(currencyroute)
app.include_router(banner_router)
app.include_router(article_router)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
templates = Jinja2Templates(directory="src/frontend/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/registration", response_class=HTMLResponse)
def registration_get(request: Request):
    return templates.TemplateResponse("registrationForm.html", {"request":request})

@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("loginForm.html", {"request":request})

@app.get("/api/verify")
async def verify_token(username: str = Depends(get_user_from_header)):
    return {"valid": True, "username": username}
