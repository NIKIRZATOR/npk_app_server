import secrets
from datetime import datetime, timedelta, timezone
import bcrypt, jwt

from .config import settings

def gen_salt() -> str:
    return secrets.token_hex(16)

def hash_password(password: str, salt: str) -> str:
    # пароль + соль => bcrypt
    return bcrypt.hashpw((password + salt).encode(), bcrypt.gensalt()).decode()

def verify_password(raw: str, salt: str, hashed: str) -> bool:
    return bcrypt.checkpw((raw + salt).encode(), hashed.encode())

def _make_jwt(payload: dict, exp: timedelta | None = None) -> str:
    body = payload.copy()
    if exp is not None:
        body["exp"] = datetime.now(timezone.utc) + exp
    return jwt.encode(body, settings.SECRET_KEY, algorithm="HS256")

def issue_tokens(user_id: int) -> dict:
    access = _make_jwt({"id": user_id}, exp=timedelta(hours=settings.ACCESS_HOURS))

    if settings.REFRESH_DAYS and settings.REFRESH_DAYS > 0:
        refresh = _make_jwt({"id": user_id, "typ": "refresh"}, exp=timedelta(days=settings.REFRESH_DAYS))
    else:
        # refresh без exp
        refresh = jwt.encode({"id": user_id, "typ": "refresh"}, settings.SECRET_KEY, algorithm="HS256")

    return {"access": access, "refresh": refresh}

def get_id_from_token(token: str) -> int:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return int(payload["id"])

