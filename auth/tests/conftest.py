# auth/tests/conftest.py
import os
import sys
from pathlib import Path

AUTH_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTH_DIR))

# тестовый режим (SQLite вместо Postgres)
os.environ["TESTING"] = "1"

from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine, get_db, SessionLocal


# создаём таблицы один раз перед всеми тестами
Base.metadata.create_all(bind=engine)


# подменяем зависимость get_db, чтобы тесты юзали наш SessionLocal
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# клиент FastAPI для тестов
import pytest


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
