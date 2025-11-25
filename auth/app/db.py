import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

class Base(DeclarativeBase):
    pass


#  ТЕСТИРОВАНИЕ: если переменная окружения TESTING == "1" — используем SQLite вместо Postgres
TESTING = os.getenv("TESTING") == "1"

if TESTING:
    DATABASE_URL = "sqlite:///./test_auth.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # для SQLite в одном процессе
    )
else:
    DATABASE_URL = (
        f"postgresql+psycopg2://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()