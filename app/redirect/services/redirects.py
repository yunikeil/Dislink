from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.redirect import models


async def get_by_server_id(db_session: AsyncSession, *, server_id: int) -> models.RedirectInfo | None:
    stmt = select(models.RedirectInfo).where(models.RedirectInfo.server_id == server_id)
    redirect: models.RedirectInfo | None = (await db_session.execute(stmt)).scalar()
    return redirect


async def get_by_domen_url(db_session: AsyncSession, *, ):
    pass


async def create_redirect(db_session: AsyncSession, *, ):
    pass


async def update_redirect(db_session: AsyncSession, *, ):
    pass

async def delete_redirect(db_session: AsyncSession, *, ):
    pass
