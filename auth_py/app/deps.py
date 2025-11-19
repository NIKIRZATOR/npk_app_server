from fastapi import Header
from .security import get_id_from_token
from .responses import unauthorized

def get_current_user_id(authorization: str | None = Header(default=None)) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        unauthorized("Нет токена")
    token = authorization.split(" ", 1)[1]
    return get_id_from_token(token)
