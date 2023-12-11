import time

import sqlalchemy
from sqlalchemy.orm import Session

from app.redirect.models import RedirectInfo as RedirModelDB
from app.redirect.schemas import RedirectInfo as RedirInfoDTO


def create_redirect(data: RedirInfoDTO, db: Session):
    redirect = RedirModelDB(
        server_id=data.server_id,
        server_link=data.server_link,
        domen_link=data.domen_link,
        last_use=int(time.time()),
    )
    try:
        db.add(redirect)
        db.commit()
        db.refresh(redirect)

    except sqlalchemy.exc.IntegrityError:
        # Что то уже существует
        return None

    return {"ok": redirect}


def get_redirect(db: Session, server_id: int = None, domen_link: str = None):
    if server_id is not None:
        redirect = (
            db.query(RedirModelDB).filter(RedirModelDB.server_id == server_id).first()
        )

    elif domen_link is not None:
        redirect = (
            db.query(RedirModelDB).filter(RedirModelDB.domen_link == domen_link).first()
        )

    else:
        return {"error": "any(server_id, domen_link) must be int, not NoneType"}

    if not redirect:
        return {"error": "There is no active redirection for this server"}  

    redirect.last_use = int(time.time())
    db.add(redirect)
    db.commit()
    db.refresh(redirect)

    return {"ok": redirect}


def update_redirect(data: RedirInfoDTO, db: Session):
    redirect = (
        db.query(RedirModelDB).filter(RedirModelDB.server_id == data.server_id).first()
    )

    if not redirect:
        return {"error": "There is no active redirection for this server"}  

    redirect.server_link = data.server_link
    redirect.domen_link = data.domen_link
    redirect.last_use = int(time.time())
    db.add(redirect)
    db.commit()
    db.refresh(redirect)

    return {"ok": redirect}


def remove_redirect(server_id: int, db: Session):
    redirect = (
        db.query(RedirModelDB).filter(RedirModelDB.server_id == server_id).delete()
    )

    if not redirect:
        return {"error": "There is no active redirection for this server"}  
    
    db.commit()

    return {"ok": redirect}


def gel_all(db: Session):
    redirects = (
        db.query(RedirModelDB).all()
    )
    
    if not redirects:
        return {"error": "There is no active redirection"}  
    
    return {"ok": redirects}

