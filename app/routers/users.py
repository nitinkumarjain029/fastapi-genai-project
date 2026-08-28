from fastapi import FastAPI, APIRouter,  HTTPException, status
from app.schemas.user import userCreate, UserResponse 


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
) 


@router.get("/{user_id}",  response_model = UserResponse)
def get_User(user_id: int):
    if user_id != 1:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User Not Found"
        )
    return {
         "id" : 1,
        "name": "nitin",
        "email": "nk@gmail.com",
        "age": 32
    }


@router.post("", response_model = UserResponse, status_code= status.HTTP_201_CREATED)
def User_create(user: userCreate):

    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }



    