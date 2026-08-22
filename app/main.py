from fastapi import FastAPI, HTTPException, status, Depends
from app.routers.users import router as users_router
 

app = FastAPI(
    title = "FastAPi Gen Ai Project",
    description = "Generating FastAPi project",
    version = "1.0.0"
)


app.include_router(users_router)

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