import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:strongpassword@localhost:5432/civic_alert_db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


