from fastapi import Depends, APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import utils
from core.settings import config
from core.database import get_session
from app import services, models


DISCORD_INVITE: str = "https://discord.gg/"
router = APIRouter(tags=["root"])


@router.get("/", include_in_schema=config.debug)
async def get_index(request: Request):
    return FileResponse("_public/index.html")


@router.get("/c/{public:path}", include_in_schema=config.debug)
async def get_public(request: Request, public: str):
    if not (file := utils.is_static(public)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return FileResponse(f"_public/{public}")


@router.get("/{domen_link}")
async def get_redirect(request: Request, domen_link: str, db_session: AsyncSession = Depends(get_session)):
    redirect: models.RedirectInfo = await services.get_by_domen_url(db_session, domen_link=domen_link)
    
    if not redirect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Redirect not found."
        )
        
    redirect = "https://discord.gg/" + redirect.server_link
    
    return RedirectResponse(redirect, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
