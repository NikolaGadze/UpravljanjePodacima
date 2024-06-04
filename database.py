from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', '3306')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'appointments')
DATABASE_USER = os.getenv('DATABASE_USER', 'user')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')

DATABASE_URL = "mysql+mysqlconnector://root:nikola911@mysql:3306/hsm"
#DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()