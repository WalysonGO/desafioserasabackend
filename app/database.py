import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.utils.env_loader import load_env

# Carrega variáveis de ambiente
load_env()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://db_user:db_pass123@localhost:5432/debts_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
