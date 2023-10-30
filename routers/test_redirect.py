from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db

from db_services import redirect_info as RedirictDB


router = APIRouter()
DISCORD_INVITE: str = "https://discord.gg/"

@router.get("/{domen_link}", tags=["test(root)"])
async def redirector(request: Request, domen_link: str, db: Session = Depends(get_db)):
    redirect_link = RedirictDB.get_redirect(db, domen_link=domen_link)
    if redirect_link:
        return RedirectResponse(DISCORD_INVITE+redirect_link.server_link, status_code=308)
    else:
        return {
            "comment": f"non-existent link={str(request.base_url)+domen_link}({type(domen_link)})",
        }
