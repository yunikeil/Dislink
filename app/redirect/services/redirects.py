from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.redirect import models, schemas


async def get_by_server_id(db_session: AsyncSession, *, server_id: int) -> models.RedirectInfo | None:
    stmt = select(models.RedirectInfo).where(models.RedirectInfo.server_id == server_id)
    redirect: models.RedirectInfo | None = (await db_session.execute(stmt)).scalar()
    return redirect


async def get_by_domen_url(db_session: AsyncSession, *, domen_link: str):
    stmt = select(models.RedirectInfo).where(models.RedirectInfo.domen_link == domen_link)
    redirect: models.RedirectInfo | None = (await db_session.execute(stmt)).scalar()
    return redirect


async def create_redirect(db_session: AsyncSession, *, obj_in: schemas.RedirectCreate):
    db_obj = models.RedirectInfo(**obj_in.model_dump(exclude_unset=True))
    
    db_session.add(db_obj)
    await db_session.commit()
    await db_session.refresh(db_obj)
    
    return db_obj


async def update_redirect(db_session: AsyncSession, *, db_obj: models.RedirectInfo, obj_in: schemas.RedirectInDB):
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    db_session.add(db_obj)
    await db_session.commit()
    await db_session.refresh(db_obj)

    return db_obj


async def delete_redirect(db_session: AsyncSession, *, server_id: int):
    stmt = select(models.RedirectInfo).where(models.RedirectInfo.server_id == server_id)
    redirect = (await db_session.execute(stmt)).scalar()
    
    if not redirect:
        return None

    await db_session.delete(redirect)
    await db_session.commit()

    return redirect
