from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    location: str
    about: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class UserResponse(BaseModel):
    name: str
    email: str
    location: str
    about: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    email: str | None = None