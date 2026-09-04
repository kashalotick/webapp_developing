from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.routers.driver import driver_router
from app.routers.race import race_router
from app.schemas import Driver, Race, DriverInRace
from app.services.repository import DriverRepository, RaceRepository, DriverInRaceRepository
from app.services.repository_serializer import RepositorySerializer

REPOSITORY_PATH = Path.cwd() / "data"


@asynccontextmanager
async def lifespan(app: FastAPI):
    driver_repo = DriverRepository()
    race_repo = RaceRepository()
    driver_in_race_repo = DriverInRaceRepository()

    serializer = RepositorySerializer("./data")
    serializer.register(driver_repo, Driver)
    serializer.register(race_repo, Race)
    serializer.register(driver_in_race_repo, DriverInRace)

    serializer.deserialize()

    yield {
        "driver_repo": driver_repo,
        "race_repo": race_repo,
        "driver_in_race_repo": driver_in_race_repo,
    }

    serializer.serialize()


app = FastAPI(lifespan=lifespan)

app.include_router(driver_router)
app.include_router(race_router)
