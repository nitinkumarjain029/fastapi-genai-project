from pydantic import BaseModel
from typing import List



# schme for different action

class userCreate(BaseModel):   #POST request ke liye
    name : str
    email : str
    age : int
    phone: str | None = None
    password: str
    role: str = "user"


class UserResponse(BaseModel):  #API response ke liye
    id: int
    name : str
    email: str
    age : int
    phone: str | None = None

class PaginatedUserResponse(BaseModel):
    items: List[UserResponse]
    total : int
    page : int
    limit : int
    total_pages : int

class UserUpdate(BaseModel):
    name : str
    email : str
    age : int
    phone: str

class UserPatch(BaseModel):     # now we can send altest one field for update
    name : str | None = None
    email: str | None = None
    age  : int | None = None
    phone: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token : str
