from fastapi import APIRouter
from app.presentation.controllers.user_controller import router as user_router

api_router = APIRouter()

# Include user routes
api_router.include_router(user_router, prefix="/users", tags=["users"]) 