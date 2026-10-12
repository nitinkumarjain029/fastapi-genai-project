from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./users.db"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread" : False}  # fastapi can manage multiple req as thread
)


SessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind = engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()  #Database ke saath kaam karne ke liye ek actual Session banao aur usko db variable mein store karo.
    try:
        yield db #Value do, lekin function ko completely finish mat karo. Function ki state temporarily pause kar do.
    finally:     # api ko db do db mai jo function kaam kar raha hai uske baad db ko close kar do.
        db.close()
