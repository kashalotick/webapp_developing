from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlalchemy import update, select, func

from app.api_config import ApiConfigDep
from app.db import DbSessionDep
from app.exceptions import BusinessException
from app.models.driver_in_race_model import DriverInRaceModel
from app.models.driver_model import DriverModel
from app.models.race_model import RaceModel
from app.schemas.driver import DriverRead, DriverCreate, DriverUpdate
from app.schemas.race import RaceRead
from app.services.repository import AbstractAsyncRepository, AsyncRepository

from app.deps import LoggerDep

class AbstractDriverRepository(AbstractAsyncRepository[DriverModel, DriverCreate, DriverUpdate, DriverRead], ABC):

    @abstractmethod
    async def change_rating(self, driver_id: int, delta: int) -> DriverRead | None:
        pass

    @abstractmethod
    async def get_driver_races(self, driver_id: int, page: int) -> list[RaceRead]:
        pass


class DriverRepository(AbstractDriverRepository, AsyncRepository):

    def __init__(self, db: DbSessionDep, logger: LoggerDep, api_config: ApiConfigDep) -> None:
        super().__init__(db, DriverModel, DriverRead, logger, api_config)
        self.db = db
        self.logger = logger.getChild(type(self).__name__)


    async def change_rating(self, driver_id: int, delta: int) -> None | DriverRead:
        query = (
            update(DriverModel)
            .where(DriverModel.id == driver_id)
            .values({
                DriverModel.rating: func.greatest(0, DriverModel.rating + delta)
            })
            .returning(DriverModel)
        )
        result = await self.db.scalar(query)
        await self.db.flush()

        if not result:
            self.logger.warning(f"Driver {driver_id} not found")
            return None
        self.logger.info(f"Driver {driver_id} rating changed by {delta}")

        return DriverRead.model_validate(result)

    async def get_driver_races(self, driver_id: int, page: int) -> list[RaceRead]:
        limit, offset = self.page(page)
        if await self.db.get(DriverModel, driver_id) is None:
            raise BusinessException.not_found(DriverModel)

        stmt = (
            select(RaceModel)
            .join(RaceModel.driver_registrations)
            .where(DriverInRaceModel.driver_id == driver_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        races = result.scalars().unique().all()

        return [RaceRead.model_validate(race) for race in races]


DriverRepoDep = Annotated[AbstractDriverRepository, Depends(DriverRepository)]
