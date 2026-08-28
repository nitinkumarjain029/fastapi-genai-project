from pydantic import BaseModel


class userCreate(BaseModel):
    name : str
    email : str
    age : int


class UserResponse(BaseModel):
    id: int
    name : str
    email: str
    age : int
