import json
import asyncio
import secrets
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

import core.settings as conf
from core.database import init_models
from app import redirect_routers


security = HTTPBasic()
app = FastAPI(
    version="0.1.0",
    title="Dislink bot",
    summary="Discord bot for creating link-shortcuts to servers.",
    openapi_tags=json.loads(open("_locales/tags_metadata.json", "r").read()), 
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

def __temp_get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"yunik"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"24011953"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/c/docs", include_in_schema=False)
async def get_swagger_documentation(
    username: str = Depends(__temp_get_current_username),
):
    return get_swagger_ui_html(openapi_url="/c/openapi.json", title="docs")


@app.get("/c/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(__temp_get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

app.include_router(redirect_routers)


if __name__ == '__main__':
    asyncio.run(init_models(drop_all=False))
    uvicorn.run("server:app", host=conf.server_ip, port=conf.server_port, reload=True)
