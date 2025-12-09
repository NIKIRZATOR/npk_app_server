from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jwt import InvalidTokenError, ExpiredSignatureError

from ..db import get_db
from ..user_model import UserModel
from ..schemas import UserAuthIn, UserSignUpIn, UserOut
from ..security import gen_salt, hash_password, verify_password, issue_tokens, get_id_from_token
from ..responses import ok, bad_request, unauthorized

router = APIRouter(prefix="/token", tags=["token"])

class RefreshIn(BaseModel):
    refresh: str

@router.post("")
def sign_in(payload: UserAuthIn, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == payload.username).first()
    if not user:
        bad_request("Пользователь не найден")

    if not verify_password(payload.password, user.salt, user.hash_password):
        bad_request("Неверный пароль")

    tokens = issue_tokens(user.id)
    user.accessToken, user.refreshToken = tokens["access"], tokens["refresh"]
    db.commit(); db.refresh(user)

    return ok(UserOut.model_validate(user), message="Успешная авторизация!")

@router.put("")
def sign_up(payload: UserSignUpIn, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.username == payload.username).first():
        bad_request("Username уже занят")

    salt = gen_salt()
    user = UserModel(
        username=payload.username,
        salt=salt,
        hash_password=hash_password(payload.password, salt),
        surName=payload.surName,
        name=payload.name,
        patronymicName=payload.patronymicName,
        jobTitle=payload.jobTitle,
        userRole=payload.userRole,
    )
    db.add(user); db.commit(); db.refresh(user)

    tokens = issue_tokens(user.id)
    user.accessToken, user.refreshToken = tokens["access"], tokens["refresh"]
    db.commit(); db.refresh(user)

    return ok(UserOut.model_validate(user), message="Успешная регистрация")

@router.post("/refresh")
def refresh_token(payload: RefreshIn, db: Session = Depends(get_db)):
    # 1 - decoding token, get id
    try:
        uid = get_id_from_token(payload.refresh)
    except (InvalidTokenError, ExpiredSignatureError):
        unauthorized("Токен не валидный или истёк")

    # 2 - find user
    user = db.query(UserModel).get(uid)
    if not user or user.refreshToken != payload.refresh:
        unauthorized("Ошибка совпадения токенов. Токен не валидный")

    # 3 - issue new tokens
    tokens = issue_tokens(uid)
    user.accessToken, user.refreshToken = tokens["access"], tokens["refresh"]
    db.commit()
    db.refresh(user)

    return ok(UserOut.model_validate(user), message="Успешное обновление токенов")
