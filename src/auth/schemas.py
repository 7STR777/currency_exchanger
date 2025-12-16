from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    username: str 
    password: str = Field(max_length=32, min_length=8)
    email: str | None = None
    role: str = "user"

class Currency(BaseModel):
    convert_to: str
    convert_from: str
    convert_amount: str

class CustomExceptionModel(BaseModel):
    status_code: int
    er_message: str
    er_details: str 

class Banner(BaseModel):
    code: str

class Article(BaseModel):
    title: str
    intro_text: str
    full_text: str
    codeimg: str = ""

class Reviews(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str