from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base   
from dotenv import load_dotenv
import os

# Carga el .env del user-service
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "users.db")
DATABASE_URL = f"sqlite:///./{DB_NAME}"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
