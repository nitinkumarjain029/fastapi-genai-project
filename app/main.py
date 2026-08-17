from fastapi import FastAPI

app = FastAPI(
    title = "FastAPi Gen Ai Project",
    description = "Generating FastAPi project",
    version = "1.0.0"
)

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
