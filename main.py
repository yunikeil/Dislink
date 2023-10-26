import uvicorn
from fastapi import FastAPI
from database import SessionLocal, engine, Base
from routers.user import router as UserRouter

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(UserRouter)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=2525, reload=True, workers=3)