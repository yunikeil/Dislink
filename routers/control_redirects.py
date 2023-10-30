from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db

from db_services import redirect_info as RedirectDB
from dto import redirect_info as RedirictDTO


router = APIRouter()
ALLOWED_IPS = ["62.113.96.70"]


def check_ip(request: Request):
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=404, detail="IP address is not allowed")


@router.post(
    "/control/redirect",
    tags=["control"],
    responses={
        200: {"model": RedirictDTO.RedirectInfo},
        400: {"model": RedirictDTO.RedirectError},
    },
)
async def create_redirect(
    request: Request,
    data: RedirictDTO.RedirectInfo,
    db: Session = Depends(get_db),
):
    check_ip(request)
    request.client.host
    result = RedirectDB.create_redirect(data, db)
    if text := result.get("error"):
        return JSONResponse({"comment": text}, status.HTTP_400_BAD_REQUEST)
    
    return result.get("ok")


@router.get(
    "/control/redirect/{id}",
    tags=["control"],
    responses={200: {"model": RedirictDTO.RedirectInfo}},
)
async def get_redirect(request: Request, id: int, db: Session = Depends(get_db)):
    check_ip(request)
    result = RedirectDB.get_redirect(db, server_id=id)

    return result


@router.put(
    "/control/redirect/{id}",
    tags=["control"],
    responses={200: {"model": RedirictDTO.RedirectInfo}},
)
async def update_redirect(
    request: Request,
    id: int,
    data: RedirictDTO.RedirectInfo,
    db: Session = Depends(get_db),
):
    check_ip(request)
    result = RedirectDB.update_redirect(id, data, db)

    return result


@router.delete(
    "/control/redirect/{id}",
    tags=["control"],
    responses={200: {"model": bool}},
)
async def remove_redirect(request: Request, id: int, db: Session = Depends(get_db)):
    check_ip(request)
    result = RedirectDB.remove_redirect(id, db)
    return bool(result)
