import sqlalchemy
from sqlalchemy.orm import Session

from db_models.redirect_info import RedirectInfo as RedirModelDB
from dto.redirect_info import RedirectInfo as RedirModelDTO


def create_redirect(data: RedirModelDTO, db: Session):
    redirect = RedirModelDB(
        server_id=data.server_id,
        server_link=data.server_link,
        domen_link=data.domen_link,
    )
    try:
        db.add(redirect)
        db.commit()
        db.refresh(redirect)

    except sqlalchemy.exc.IntegrityError as e:
        error_messages = {
            "UNIQUE constraint failed: RedirectInfo.server_id": f"server_id={data.server_id}({type(data.server_id)}, primary_key=True) already exists",
            "UNIQUE constraint failed: RedirectInfo.server_link": f"server_link={data.server_link}({type(data.server_link)}, unique=True) already exists",
            "UNIQUE constraint failed: RedirectInfo.domen_link": f"domen_link={data.domen_link}({type(data.domen_link)}, unique=True) already exists",
        }
        return { "error": error_messages.get(str(e.orig))}

    return { "ok": redirect }


def get_redirect(db: Session, server_id: int = None, server_link: str = None, domen_link: str = None):
    if server_id is not None:
        return db.query(RedirModelDB).filter(RedirModelDB.server_id == server_id).first()
    
    if server_link is not None:
        return (
            db.query(RedirModelDB)
            .filter(RedirModelDB.server_link == server_link)
            .first()
        )

    if domen_link is not None:
        return (
            db.query(RedirModelDB)
            .filter(RedirModelDB.domen_link == domen_link)
            .first()
        )
    
    raise "server_id must be int, not NoneType"    


def update_redirect(server_id: int, data: RedirModelDTO, db: Session):
    redirect = (
        db.query(RedirModelDB).filter(RedirModelDB.server_id == server_id).first()
    )
    redirect.server_link = data.server_link
    redirect.domen_link = data.domen_link
    db.add(redirect)
    db.commit()
    db.refresh(redirect)
    
    return redirect


def remove_redirect(server_id: int, db: Session):
    redirect = (
        db.query(RedirModelDB).filter(RedirModelDB.server_id == server_id).delete()
    )
    db.commit()

    return redirect
