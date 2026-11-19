from fastapi import APIRouter

client_router = APIRouter(prefix="", tags=["CLient"])


@client_router.get("/races")
async def get_races_page():
    return {"ping": "pong"}

@client_router.get("/races/{race_id}")
async def get_race_page_by_id(race_id: int):
    return {"ping": "pong"}

@client_router.get("/drivers")
async def get_drivers_page():
    return {"ping": "pong"}


@client_router.get("/drivers/{driver_id}")
async def get_driver_page_by_id(driver_id: int):
    return {"ping": "pong"}



@client_router.get("/races/{race_id}/drivers")
async def get_race_drivers(race_id: int):
    return {"ping": "pong"}


@client_router.get("/drivers/{driver_id}/races")
async def get_driver_races(driver_id: int):
    return {"ping": "pong"}