from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id =    Column(Integer, primary_key=True, index= True)
    name =  Column(String, nullable = False)
    email = Column(String, unique =True, nullable=False, index=True)
    age =   Column(Integer, nullable=False)
    phone = Column(String, nullable = True)
    password = Column(String, nullable = False)
    role = Column(String, nullable = False, default = "user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
