import json

import uvicorn
from fastapi import FastAPI

from database import engine, Base
from routers import control_redirects, usage_redirects
import configuration


Base.metadata.create_all(bind=engine)
ROUTETRS = [control_redirects, usage_redirects]

app = FastAPI(
    version="0.1.0",
    title="Dislink bot",
    summary="Discord bot for creating link-shortcuts to servers.",
    openapi_tags=json.loads(open("_locales/tags_metadata.json", "r").read()), 
    docs_url="/control/docs",
    redoc_url="/control/redocs",
    openapi_url="/control/openapi.json"
)

for part in ROUTETRS:
    app.include_router(part.router)

if __name__ == '__main__':
    uvicorn.run("server:app", host=configuration.server_ip, port=configuration.server_port, reload=True)
