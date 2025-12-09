from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_current_user_id
from ..db import get_db
from ..user_model import UserModel
from ..responses import ok, not_found

router = APIRouter(prefix="/user", tags=["user"])

@router.get("")
def get_me(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(UserModel).get(user_id)
    if not user:
        not_found("Пользователь не найден")
    # TODO добавь нужные поля
    return ok({"id": user.id, "username": user.username})


## TODO getUserProfile, updateUserProfile, updateUserPassword, getAllUsers
