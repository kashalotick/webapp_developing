from fastapi import FastAPI

from app.routers.driver import driver_router
from app.routers.race import race_router

app = FastAPI()

app.include_router(driver_router)
app.include_router(race_router)
