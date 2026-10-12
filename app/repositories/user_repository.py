from sqlalchemy.orm import Session
from app.db.models import User



def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

## new user banaane ke liye

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db : Session, skip : int = 0, limit: int = 10):
    query = db.query(User)
    total = query.count()

    items = (
        query.offset(skip).limit(limit).all()
    )

    return total, items

## update one user

def update_user(db: Session, db_user: User, update_user: dict):

    for key, value in update_user.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

 # delelte user

def delete_user(db:Session, db_user : User):
    db.delete(db_user)
    db.commit()

#for login api find user through email

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
