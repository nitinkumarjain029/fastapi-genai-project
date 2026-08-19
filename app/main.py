from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
 

app = FastAPI(
    title = "FastAPi Gen Ai Project",
    description = "Generating FastAPi project",
    version = "1.0.0"
)

class User(BaseModel):
    name: str
    email:str
    age: int
    phoneNo: Optional[str] = None

@app.post("/user")
def create_user(user: User):
    return {
        "message": "User Create Successfully REE",
        "user": user
    }   

@app.get("/")
def home():
    return {
        "message": "Hi All This is Gen Ai Project"
    }

@app.get("/hello")
def hello():
    return {
        "message": "hello not radhe radhe"
    }

@app.get("/users/{user_id}")
def get_user(user_id : int):
    return {
        "user_id": user_id
    }

@app.get("/search")
def search_user(name : str):
    return {
        "seraching for": name
    }

@app.post("/users")
def create_users():
    return {
        "messge":  "User created successfully"
    }   

