from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    display_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
class Token(BaseModel):
    token: str
class oAuthResponse(BaseModel):
    token: str
    uid: int
    username: str
    display_name: str

