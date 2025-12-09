from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .db import Base, engine
from .config import settings
from .routes import token, user

from .user_model import UserModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # when app is starting
    Base.metadata.create_all(bind=engine)
    print("DB initialized (create_all)")

    yield

    # when app is shutting down
    print("App shutdown")


app = FastAPI(
    title="auth",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(token.router)
app.include_router(user.router)
