from fastapi import APIRouter

from .routers import control_redirects


redirect_routers = APIRouter(tags=["redirect"])
redirect_routers.include_router(control_redirects.router)
