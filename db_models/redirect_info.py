from sqlalchemy import Column, Integer, String
from database import Base


class RedirectInfo(Base):
    __tablename__ = "RedirectInfo"

    server_id = Column(Integer, unique=True, index=True)
    server_link = Column(String, unique=True, index=True)
    domen_link = Column(String, unique=True, index=True)
