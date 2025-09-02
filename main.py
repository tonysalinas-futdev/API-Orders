from fastapi import FastAPI
from routes import router
import database 
from init_status import init_status




app=FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    async with database.AsyncLocalSession() as session:
        await init_status(session)
