from fastapi import FastAPI, HTTPException, status, Depends
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
    password : str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


@app.post("/user", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(user: User):
    return {
        "id": 1,
        "name": user.name,
        "emami": user.email,
        "age": user.age,
        "password": "secret123"


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

@app.get("/users/{user_id}", response_model = UserResponse)
def get_user(user_id:int):
    if user_id != 1:
         raise HTTPException(
             status_code = 404,
             detail = "User Not Found"
         )

    return {
        "id":1,
        "name": "nit",
        "email": "mm@gmail.com",
        "age": 23
    }


def get_current_user():
    return {
        "id": 1,
        "name": "Ram",
        "role": "Admin"
    }

@app.get("/profile")
def profile(user = Depends(get_current_user)):
    return {
        "message": "Admin Data Fetch",
        "user": user
       
    }

def get_role_user():
    role = "Admin"
    return role

@app.get("/roles")
def get_role(role = Depends(get_role_user)):
    if role != "Admin":
        raise HTTPException(
            status_code = 403,
            detail = "ADMIN Access Denied"
        )
    return {
        "message": "Welcome Admin"
    }