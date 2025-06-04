# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = "postgresql://postgres:"+os.getenv("DB_PASSWORD")+"@"+DB_HOST+":5432/"+DB_NAME

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # Base class for all models