from fastapi import FastAPI

from api import routers


app = FastAPI()
app.include_router(routers.databases.router)




@app.get("/")
async def root():
    return {"Hello": "World"}
