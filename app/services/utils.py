
from fastapi import HTTPException
from starlette import status

from app.schemas import Race, Driver
from app.services.repository import RaceRepository, DriverRepository


def get_race_or_404(race_id: int, race_repo: RaceRepository) -> Race:
    race = race_repo.get(race_id)
    if race is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return race


def get_driver_or_404(driver_id: int, driver_repo: DriverRepository) -> Driver:
    driver = driver_repo.get(driver_id)
    if driver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return driver



