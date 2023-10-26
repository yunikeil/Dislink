from sqlalchemy.orm import Session

from db_models.redirect_info import RedirectInfo as RedirModelDB
from dto.redirect_info import RedirectInfo as RedirModelDTO


def create_redirect(data: RedirModelDTO, db: Session):
    redirect = RedirModelDB(server_link=data.server_link, domen_link=data.domen_link)
    try:
        db.add(redirect)
        db.commit()
        db.refresh(redirect)
    except Exception as e:
        print(e)
    return redirect


def get_redirect(server_id: int, db: Session):
    return db.query(RedirModelDB).filter(RedirModelDB.server_id == server_id).first()


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
