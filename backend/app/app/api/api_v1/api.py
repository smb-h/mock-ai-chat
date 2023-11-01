from fastapi import APIRouter

from app.api.api_v1.endpoints import interactions, login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    interactions.router, prefix="/interactions", tags=["interactions"]
)
