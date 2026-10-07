from fastapi import APIRouter
from routes.health_routes import router as health_router
from routes.project import router as project_router
from routes.auth_rotues import router as auth_router
api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(project_router)

api_router.include_router(auth_router)