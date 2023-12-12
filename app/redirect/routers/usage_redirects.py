import os

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session



DISCORD_INVITE: str = "https://discord.gg/"
router = APIRouter(tags=["root"])


@router.get("/")
async def get_index(request: Request):
    return FileResponse("_public/index.html")

