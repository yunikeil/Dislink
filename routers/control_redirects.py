from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from services.authentication import IpCheck
from services import redirect_info as RedirectDB
from dto import redirect_info as RedirictDTO
import configuration


checker = IpCheck(allowed_ips=configuration.control_redirects_allowed_ips)
router = APIRouter(
    prefix="/control",
    tags=["redirect"],
    dependencies=[Depends(checker.is_ip_allowed)],
    responses={403: {"model": RedirictDTO.RedirectError}},
)


@router.post(
    "/redirect",
    responses={
        200: {"model": RedirictDTO.RedirectInfo},
    },
)
async def create_redirect(
    request: Request,
    data: RedirictDTO.RedirectInfo,
    db: Session = Depends(get_db),
):      
    request.client.host
    result = RedirectDB.create_redirect(data, db)
    if text := result.get("error"):
        return JSONResponse({"detail": text}, status_code=403)

    return result.get("ok")


@router.get(
    "/redirect/{id}",
    responses={200: {"model": RedirictDTO.RedirectInfo}},
)
async def get_redirect(request: Request, id: int, db: Session = Depends(get_db)):
    result = RedirectDB.get_redirect(db, server_id=id)
    if text := result.get("error"):
        return JSONResponse({"detail": text}, status_code=403)

    return result.get("ok")


@router.put(
    "/redirect",
    responses={200: {"model": RedirictDTO.RedirectInfo}},
)
async def update_redirect(
    request: Request,
    data: RedirictDTO.RedirectInfo,
    db: Session = Depends(get_db),
):
    result = RedirectDB.update_redirect(data, db)
    if text := result.get("error"):
        return JSONResponse({"detail": text}, status_code=403)

    return result.get("ok")


@router.delete(
    "/redirect/{id}",
    responses={200: {"model": bool}},
)
async def remove_redirect(request: Request, id: int, db: Session = Depends(get_db)):
    result = RedirectDB.remove_redirect(id, db)
    if text := result.get("error"):
        return JSONResponse({"detail": text}, status_code=403)
    
    return result.get("ok")
