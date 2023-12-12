from fastapi import APIRouter

from .routers import control_redirects, usage_redirects


redirect_routers = APIRouter()
redirect_routers.include_router(control_redirects.router)
redirect_routers.include_router(usage_redirects.router)
