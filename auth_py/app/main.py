from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .config import settings
from .routes import token, user

app = FastAPI(title="auth_py")

# CORS (для Flutter Web/ локальных стендов)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token.router)
app.include_router(user.router)
#app.include_router(user_info.router)
