from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.deps import DriverRepoDep, RaceRepoDep, \
    DriverInRaceRepoDep
from app.schemas import Driver, RatingDelta, Race, DriverCreate, DriverUpdate
from app.services.utils import get_driver_or_404

driver_router = APIRouter(prefix="/drivers")


@driver_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Driver)
async def create(body: DriverCreate, driver_repo: DriverRepoDep) -> Driver:
    driver = Driver(**body.model_dump())
    return driver_repo.add(driver)


@driver_router.get("/", response_model=list[Driver])
async def get_all(driver_repo: DriverRepoDep) -> list[Driver]:
    return driver_repo.get_all()


@driver_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(driver_repo: DriverRepoDep, driver_in_race_repo: DriverInRaceRepoDep):
    driver_repo.clear()
    driver_in_race_repo.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@driver_router.get("/{driver_id}", response_model=Driver, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_by_id(driver_id: int, driver_repo: DriverRepoDep) -> Driver:
    driver = get_driver_or_404(driver_id, driver_repo)
    return driver


@driver_router.patch("/{driver_id}", response_model=Driver, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def patch_by_id(driver_id: int, body: DriverUpdate, driver_repo: DriverRepoDep) -> Driver:
    driver = get_driver_or_404(driver_id, driver_repo)
    update_data = body.model_dump(exclude_unset=True)
    updated_driver = driver.model_copy(update=update_data)
    return driver_repo.set(driver_id, updated_driver)


@driver_router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(driver_id: int, driver_repo: DriverRepoDep, driver_in_race_repo: DriverInRaceRepoDep):
    driver_repo.delete(driver_id)
    registrations = driver_in_race_repo.get_all()
    for reg in registrations:
        if reg.driver_id == driver_id:
            driver_in_race_repo.delete(reg.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@driver_router.get("/{driver_id}/races", response_model=list[Race], responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_all_races(
        driver_id: int,
        driver_repo: DriverRepoDep,
        race_repo: RaceRepoDep,
        driver_in_race_repo: DriverInRaceRepoDep
) -> list[Race]:
    driver = get_driver_or_404(driver_id, driver_repo)
    all_race_registrations = driver_in_race_repo.get_all()

    races: list[Race] = []

    for reg in all_race_registrations:
        if reg.driver_id == driver.id:
            race = race_repo.get(reg.race_id)
            if race is not None:
                races.append(race)

    return races


@driver_router.post("/{driver_id}/rating/change", response_model=Driver, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def change_rating(
        driver_id: int,
        body: RatingDelta,
        driver_repo: DriverRepoDep
) -> Driver:
    driver = get_driver_or_404(driver_id, driver_repo)
    driver.rating += body.delta
    return driver_repo.set(driver_id, driver)
