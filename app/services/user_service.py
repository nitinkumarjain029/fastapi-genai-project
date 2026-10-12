from app.schemas.user import userCreate, UserUpdate, UserPatch
from fastapi import  HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.models import User, RefreshToken
from app.core.exceptions import UserNotFoundException, EmailAlreadyExistsException, InvalidCredentialsException
from sqlalchemy.exc import IntegrityError
from app.repositories.user_repository import get_user_by_id
from app.repositories.user_repository import create_user, get_all_users,  update_user as update_user_repository, delete_user as delete_user_repository, get_user_by_email
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS
from app.repositories.refresh_token_repository import create_refresh_token as save_refresh_token, get_refresh_token, revoke_refresh_token
from datetime import datetime, timedelta, timezone
import math
# service ko actual database se connect karenge


def create_user_service(db: Session, user: userCreate):

    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        age=user.age,
        phone=user.phone,
        password=hashed_password,
        role=user.role
    )
    return create_user(db, db_user)

    # except IntegrityError:

    #     db.rollback()

    # raise EmailAlreadyExistsException()

# for get user api

def get_user_service(db : Session, user_id: int):
    user = get_user_by_id(db, user_id)


    if user is None:
        raise UserNotFoundException()

    return user

# get All users

def get_all_users_service(db:Session, page : int =1, limit : int = 10):
    skip = (page - 1) * limit
    total, items =  get_all_users(db, skip= skip, limit = limit)
    total_pages = math.ceil(total / limit)
    return {
        "items" : items,
        "total" : total,
        "page" : page,
        "limit" : limit,
        "total_pages" :total_pages
    }


# user Update

def update_user(db: Session, user_id : int, user : UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        return None

    db_user.name = user.name            #  user client side or db_user database side
    db_user.email = user.email
    db_user.age = user.age

    db.commit()
    db.refresh(db_user)

    return db_user

#delete user

def delete_user_service(user_id: int, db : Session):
    try:
        db_user =  get_user_by_id(db, user_id)

        if db_user is None:
            raise UserNotFoundException()

        delete_user_repository(db, db_user)

    except Exception as e:
        db.rollback()
        raise e

# user patch update at lest one field


def update_user_service(user_id: int, db: Session, user: UserPatch):
    db_user = get_user_by_id(db, user_id)

    if db_user is None:
        raise UserNotFoundException()

    update_data = user.model_dump(exclude_unset=True)

    try:
        return update_user_repository(db, db_user, update_data)
    except IntegrityError as e:
        db.rollback()
        raise EmailAlreadyExistsException() from e


def login_service(db: Session, email: str, password: str):
    db_user = get_user_by_email(db, email)

    if db_user is None:
        raise InvalidCredentialsException()

    password_valid = verify_password(
        password,
        db_user.password
    )

    if not password_valid:
        raise InvalidCredentialsException()

    access_token = create_access_token(
        {"sub": str(db_user.id)}
    )

    refresh_token = create_refresh_token(
        {"sub" : str(db_user.id)}
    )

    refresh_expires_at = (datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    save_refresh_token(
        db =db,
        user_id = db_user.id,
        token = refresh_token,
        expires_at = refresh_expires_at
    )

    return {
        "access_token" : access_token,
        "refresh_token": refresh_token
    }


def refresh_access_token(db: Session, refresh_token: str):

    try:
        payload = decode_refresh_token(refresh_token)

        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidCredentialsException()

        db_token = get_refresh_token(
            db=db,
            token=refresh_token
        )

        if db_token is None:
            raise InvalidCredentialsException()

        if db_token.revoked:
            raise InvalidCredentialsException()

        db_user = get_user_by_id(
            db,
            int(user_id)
        )

        if db_user is None:
            raise InvalidCredentialsException()

        access_token = create_access_token(
            {"sub": str(db_user.id)}
        )

        return access_token

    except JWTError:
        raise InvalidCredentialsException()


def logout_user(db:Session, refresh_token:str):
    db_token = revoke_refresh_token(
               db,
               refresh_token
    )
    if db_token is None:
        raise InvalidCredentialsException()

    return True
