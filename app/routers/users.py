from fastapi import FastAPI, APIRouter,  HTTPException, status, Depends
from app.schemas.user import userCreate, UserResponse, UserUpdate, UserPatch, LoginRequest, RefreshTokenRequest, PaginatedUserResponse
from app.services.user_service import create_user_service, get_user_service, get_all_users_service, update_user, delete_user_service, update_user_service, login_service, refresh_access_token, logout_user
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.exceptions import InvalidCredentialsException
from app.dependencies.auth import get_current_user, get_current_admin
from app.repositories.refresh_token_repository import get_refresh_token
from fastapi import Query


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)


#get all Users

@router.get("", response_model= PaginatedUserResponse)
def get_all_users_endpoint(page: int = Query(1, ge=1), limit : int = Query(10, ge=1 , le = 100),  db:Session = Depends(get_db)):
    return get_all_users_service(db = db, page =page, limit = limit)

#get one User by id

@router.get("/me", response_model = UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model = UserResponse)
def get_user( user_id: int, db:Session = Depends(get_db)):
    return get_user_service(db, user_id)

#create user

@router.post("", response_model = UserResponse, status_code= status.HTTP_201_CREATED)
def create_user_endpoint(user : userCreate, db: Session = Depends(get_db)):
    return create_user_service(db,user)


#put endpoint

@router.put("/{user_id}", response_model=UserResponse)
def user_update_endpoint(user_id : int,
 user: UserUpdate,
 db : Session = Depends(get_db)
 ):
    updated_user = update_user(db, user_id, user)

    if updated_user is None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "User Not Found"
        )

    return updated_user



@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def del_user_endpoint(user_id:int, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    del_user = delete_user_service(user_id,  db)
    return None

@router.patch("/{user_id}", response_model = UserResponse)
def patch_user_endpoint(user_id: int, user:UserPatch, db: Session = Depends(get_db)):
    return update_user_service(user_id, db, user)

@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    try:
        tokens = login_service(
            db,
            user.email,
            user.password
        )

        return {
            "access_token": tokens["access_token"],
            "refresh_token" : tokens["refresh_token"],
            "token_type": "bearer"
        }

    except InvalidCredentialsException:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "invalid email and password"
        )



@router.post("/refresh")
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    try:
        access_token = refresh_access_token(
            db,
            request.refresh_token
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.post("/logout")
def logout(
    request : RefreshTokenRequest,
    db : Session = Depends(get_db)
):

    try:
        logout_user(
            db,
            request.refresh_token
        )

        return {
            "message" : "Log out Successfully"
        }
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
