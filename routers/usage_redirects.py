import os

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from database import get_db
from dto import redirect_info as RedirictDTO
from services import redirect_info as RedirictDB
from services.static import is_static


DISCORD_INVITE: str = "https://discord.gg/"
router = APIRouter(
    tags=["root"],
    responses={404: {"model": RedirictDTO.RedirectError}},
)

@router.get("/")
async def get_index(request: Request):
    return FileResponse("_public/index.html")


@router.get("/{domen_link:path}")
async def redirector(request: Request, domen_link: str, db: Session = Depends(get_db)):
    # ! error in other routers: "non-existent link: https://dislink.space/control/redirect/1169354124299603978" in control.get_redirect

    if static_path := is_static(domen_link):
        return FileResponse(static_path)
    
    redirect_link = RedirictDB.get_redirect(db, domen_link=domen_link)

    if data := redirect_link.get("ok"):
        return RedirectResponse(DISCORD_INVITE+data.server_link, status_code=301)
    else:
        return JSONResponse({
            "detail": f"non-existent link: {str(request.base_url)+domen_link}",
        }, status_code=404)
