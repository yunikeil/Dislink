import os

from pydantic import BaseModel, validator


class RedirectInfo(BaseModel):
    server_id: int
    server_link: str
    domen_link: str

    @validator("domen_link", always=True)
    def validate_date(cls, value: str):
        forbidden = []
        for _, _, files in os.walk("_public"):
            for name in files:
                forbidden.append(name)
        if value in forbidden:
            # Verification is carried out on the side of the bot
            # I'm not quite sure exactly how the verification of links should be done
            pass

        return value


class RedirectError(BaseModel):
    detail: str
