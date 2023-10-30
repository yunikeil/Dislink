import uvicorn
from fastapi import FastAPI

from database import SessionLocal, engine, Base
from routers import control_redirects, test_redirect


Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url="/redirect/docs", redoc_url="/redirect/redocs")

app.include_router(control_redirects.router)
app.include_router(test_redirect.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=2525, reload=True)
