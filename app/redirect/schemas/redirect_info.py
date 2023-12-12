from pydantic import BaseModel


class RedirectCreate(BaseModel):
    server_id: int
    server_link: str
    domen_link: str


class RedirectUpdate(BaseModel):
    server_link: str
    domen_link: str


class RedirectInDB(RedirectCreate):
    id: int