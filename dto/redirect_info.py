from pydantic import BaseModel


class RedirectInfo(BaseModel):
    server_id: int
    server_link: str
    domen_link: str


class RedirectError(BaseModel):
    detail: str
