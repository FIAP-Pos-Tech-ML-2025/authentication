from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str
    
class UserLoginRequest(BaseModel):
    username: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserRegisterResponse(BaseModel):
    username: str
    email: EmailStr
    message: str = "User registered successfully"
