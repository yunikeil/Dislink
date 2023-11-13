import uvicorn
import json

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from routers import control_redirects
from services import redirect_info as RedirictDB


Base.metadata.create_all(bind=engine)
DISCORD_INVITE: str = "https://discord.gg/"
ROUTETRS = [control_redirects]

app = FastAPI(
    version="0.1.0",
    title="Dislink bot",
    summary="Discord bot for creating link-shortcuts to servers.",
    openapi_tags=json.loads(open("_locales/tags_metadata.json", "r").read()), 
    docs_url="/control/docs",
    redoc_url="/control/redocs",
    openapi_url="/control/openapi.json"
)


@app.get("/{domen_link}")
async def redirector(request: Request, domen_link: str, db: Session = Depends(get_db)):
    redirect_link = RedirictDB.get_redirect(db, domen_link=domen_link)
    if redirect_link:
        return RedirectResponse(DISCORD_INVITE+redirect_link.server_link, status_code=301)
    else:
        return JSONResponse({
            "detail": f"non-existent link={str(request.base_url)+domen_link}({type(domen_link)})",
        }, status_code=404)

for part in ROUTETRS:
    app.include_router(part.router)

app.mount("/", StaticFiles(directory="_public", html=True))

if __name__ == '__main__':
    uvicorn.run("server:app", host='127.0.0.1', port=2525, reload=True)
