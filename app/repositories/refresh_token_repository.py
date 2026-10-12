from sqlalchemy.orm import Session
from app.db.models import RefreshToken

def create_refresh_token(
    db : Session,
    user_id : int,
    token : str,
    expires_at : int
):

    db_token = RefreshToken(
        user_id = user_id,
        token = token,
        expires_at = expires_at
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def get_refresh_token(
    db: Session,
    token : str
):
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def revoke_refresh_token(
    db : Session,
    token : str
):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if db_token is None:
        return None

    db_token.revoked = True
    db.commit()
    db.refresh(db_token)
    return db_token
