from pydantic import BaseModel


class RedirectInfo(BaseModel):
    server_link: str
    domen_link: str
