from pydantic import Field, BaseModel


class RedirectCreate(BaseModel):
    server_id: int
    server_link: str
    domen_link: str | None = Field(
        examples=["server"],
        min_length=2,
        max_length=30,
        pattern=r"^\D[а-яА-Яa-zA-Z0-9_-]+$",
    )


class RedirectUpdate(BaseModel):
    server_link: str | None = None
    domen_link: str | None = Field(
        examples=["server"],
        min_length=2,
        max_length=30,
        pattern=r"^\D[а-яА-Яa-zA-Z0-9_-]+$",
        default=None,
    )


class RedirectInDB(RedirectCreate):
    id: int