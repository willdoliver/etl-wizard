
from fastapi import Depends, FastAPI, Depends
from api.routers import get_routers
from .dependencies import get_query_token, get_token_header

app = FastAPI()

routers = get_routers()
dependency = [Depends(get_token_header)]

for router in routers:
    app.include_router(router, dependencies=dependency)

@app.get("/")
async def root():
    return {"status": True, "message": "Alive :)"}
