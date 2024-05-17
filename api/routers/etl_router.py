from fastapi import APIRouter, Depends
from ..dependencies import get_token_header
from api.controllers.etl_controller import ETLController

etl_controller = ETLController()

router = APIRouter(
    prefix="/etl",
    tags=["etl"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found my dear"}},
)

@router.get("/sync_data/")
async def sync_data():
    return etl_controller.sync_data()
