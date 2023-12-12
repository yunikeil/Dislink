from typing import List

from fastapi import Depends, APIRouter, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from core.security import IpCheck
from core.settings import config
from app.redirect import services, schemas, models



checker = IpCheck(allowed_ips=config.control_redirects_allowed_ips)
router = APIRouter(dependencies=[Depends(checker.is_ip_allowed)], tags=["redirect"], prefix="/c")


@router.post(path="/redirect")
async def create_redirect(request: Request, data: schemas.RedirectCreate, db_session: AsyncSession = Depends(get_session)):
    if await services.get_by_domen_url(db_session, domen_link=data.domen_link):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="domen_already_exist",
        )
    
    if await services.get_by_server_id(db_session, server_id=data.server_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="redirect_already_exist",
        )
    
    redirect = await services.create_redirect(db_session, obj_in=data)
    
    return redirect


@router.get(path="/redirect")
async def get_redirect(request: Request, server_id: int, db_session: AsyncSession = Depends(get_session)):
    redirect = await services.get_by_server_id(db_session, server_id=server_id)
    
    if not redirect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="redirect_not_exist."
        )
    
    return redirect


@router.put(path="/redirect")
async def update_redirect(request: Request, server_id: int, data: schemas.RedirectUpdate, db_session: AsyncSession = Depends(get_session)):
    redirect = await services.get_by_server_id(db_session, server_id=server_id)
    
    if not redirect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="redirect_not_exist."
        )
    
    update_data = data.model_dump(exclude_unset=True)
    
    if update_data.get("server_link") == redirect.server_link:
        del update_data["server_link"]
    
    if update_data.get("domen_link") == redirect.domen_link:
        del update_data["domen_link"]
        
    if update_data.get("domen_link"):
        if await services.get_by_domen_url(db_session, domen_link=data.domen_link):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="domen_already_exist"
            )
    
    new_redirect = await services.update_redirect(db_session, db_obj=redirect, obj_in=data)
    
    return new_redirect


@router.delete(path="/redirect")
async def delete_redirect(request: Request, server_id: int, db_session: AsyncSession = Depends(get_session)):
    redirect = await services.get_by_server_id(db_session, server_id=server_id)
    
    if not redirect:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="redirect_not_exist"
        )
    
    deleted = await services.delete_redirect(db_session, db_obj=redirect)
    
    return deleted

    