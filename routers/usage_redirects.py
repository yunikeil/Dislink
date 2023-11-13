import os

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from database import get_db
from dto import redirect_info as RedirictDTO
from services import redirect_info as RedirictDB
from services.static import get_static_files


DISCORD_INVITE: str = "https://discord.gg/"
router = APIRouter(
    tags=["root"],
    responses={404: {"model": RedirictDTO.RedirectError}},
)


@router.get("/")
async def get_index(request: Request):
    return FileResponse("_public/index.html")


@router.get("/{domen_link}")
async def redirector(request: Request, domen_link: str, db: Session = Depends(get_db)):
    static = get_static_files()
    if domen_link in static:
        return FileResponse(domen_link)
            
    redirect_link = RedirictDB.get_redirect(db, domen_link=domen_link)

    if text := redirect_link.get("ok"):
        return RedirectResponse(DISCORD_INVITE+text, status_code=301)
    else:
        return JSONResponse({
            "detail": f"non-existent link: {str(request.base_url)+domen_link}",
        }, status_code=404)
