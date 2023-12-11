from sqlalchemy import Column, Integer, String

from core.database import Base


class RedirectInfo(Base):
    __tablename__ = "RedirectInfo"

    server_id = Column(Integer, primary_key=True, index=True)
    server_link = Column(String, unique=True, index=True)
    domen_link = Column(String, unique=True, index=True)
    last_use = Column(Integer, unique=False, default=None)
