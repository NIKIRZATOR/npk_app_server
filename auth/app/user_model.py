from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # пароль храним как hash(password+salt)
    salt: Mapped[str] = mapped_column(String(120), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(200), nullable=False)

    # профиль
    surName: Mapped[str | None] = mapped_column(String(150))
    name: Mapped[str | None] = mapped_column(String(150))
    patronymicName: Mapped[str | None] = mapped_column(String(150))
    jobTitle: Mapped[str | None] = mapped_column(String(200))
    userRole: Mapped[str | None] = mapped_column(String(50))

    # токены для работы с API
    accessToken: Mapped[str | None] = mapped_column(Text)
    refreshToken: Mapped[str | None] = mapped_column(Text)
