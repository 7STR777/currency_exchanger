from pydantic import BaseModel, field_validator,Field

class User(BaseModel):
    username: str 
    password: str = Field(max_length=32, min_length=8)

class Currency(BaseModel):
    convert_to: str
    convert_from: str
    convert_amount: str

class CustomExceptionModel(BaseModel):
    status_code: int
    er_message: str
    er_details: str 

