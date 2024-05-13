from fastapi import APIRouter

from .routers import control_redirect, usage_redirect


redirect_routers = APIRouter()
redirect_routers.include_router(control_redirect.router)
redirect_routers.include_router(usage_redirect.router)
