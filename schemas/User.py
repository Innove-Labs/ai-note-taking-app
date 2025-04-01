from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserSignup(UserBase):
    password: str
    confirm_password: str
    full_name: str

class UserLogin(UserBase):
    password: str