import uvicorn
import json
from fastapi import FastAPI

from database import engine, Base
from routers import control_redirects, test_redirect


Base.metadata.create_all(bind=engine)
app = FastAPI(
    version="0.1.0",
    title="Dislink bot",
    summary="Discord bot for creating link-shortcuts to servers.",
    openapi_tags=json.loads(open("_public/tags_metadata.json", "r").read()), 
    docs_url="/control/docs",
    redoc_url="/control/redocs",
    openapi_url="/control/openapi.json"
)

app.include_router(control_redirects.router)
app.include_router(test_redirect.router)

if __name__ == '__main__':
    uvicorn.run("server:app", host='127.0.0.1', port=2525, reload=True)
