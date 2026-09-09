from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services.driver_repository import DriverRepository, AbstractDriverRepository
from app.services.race_repository import RaceRepository, AbstractRaceRepository

DbSessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_driver_repo(db: DbSessionDep) -> AbstractDriverRepository:
    return DriverRepository(db)


def get_race_repo(db: DbSessionDep) -> AbstractRaceRepository:
    return RaceRepository(db)


DriverRepoDep = Annotated[AbstractDriverRepository, Depends(get_driver_repo)]
RaceRepoDep = Annotated[AbstractRaceRepository, Depends(get_race_repo)]
