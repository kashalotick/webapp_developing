from typing import Annotated

from fastapi import Depends, Request

from app.services.repository import DriverRepository, RaceRepository, DriverInRaceRepository


def get_driver_repo(request: Request) -> DriverRepository:
    return request.state.driver_repo

def get_race_repo(request: Request) -> RaceRepository:
    return request.state.race_repo


def get_driver_in_race_repo(request: Request) -> DriverInRaceRepository:
    return request.state.driver_in_race_repo

DriverRepoDep = Annotated[DriverRepository, Depends(get_driver_repo)]
RaceRepoDep = Annotated[RaceRepository, Depends(get_race_repo)]
DriverInRaceRepoDep = Annotated[DriverInRaceRepository, Depends(get_driver_in_race_repo)]
