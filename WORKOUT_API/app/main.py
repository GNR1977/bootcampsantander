from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings

from app.routers import auth, athletes, wods, heats, scores, leaderboard, ws

class Settings(BaseSettings):
    APP_NAME: str = "CrossFit API"
    CORS_ORIGINS: list[str] = ["*"]
    ENV: str = "dev"
    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(athletes.router)
app.include_router(wods.router)
app.include_router(heats.router)
app.include_router(scores.router)
app.include_router(leaderboard.router)
app.include_router(ws.router)

@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "env": settings.ENV}