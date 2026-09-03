from urllib.error import HTTPError

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.deps import DriverRepoDep, RaceRepoDep, DriverInRaceRepoDep
from app.schemas import Race, Driver, RaceCreate, RaceUpdate, DriverInRace, DriverRegistration
from app.services.utils import get_race_or_404, get_driver_or_404

race_router = APIRouter(prefix="/races")


@race_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Race)
async def create(body: RaceCreate, race_repo: RaceRepoDep) -> Race:
    race = Race(**body.model_dump())
    return race_repo.add(race)


@race_router.get("/", response_model=list[Race])
async def get_all(race_repo: RaceRepoDep) -> list[Race]:
    return race_repo.get_all()


@race_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(race_repo: RaceRepoDep, driver_in_race_repo: DriverInRaceRepoDep):
    race_repo.clear()
    driver_in_race_repo.clear()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@race_router.get("/{race_id}", response_model=Race, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_by_id(race_id: int, race_repo: RaceRepoDep) -> Race:
    race = get_race_or_404(race_id, race_repo)
    return race


@race_router.patch("/{race_id}", response_model=Race, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def patch_by_id(race_id: int, body: RaceUpdate, race_repo: RaceRepoDep) -> Race:
    race = get_race_or_404(race_id, race_repo)
    update_data = body.model_dump(exclude_unset=True)
    updated_race = race.model_copy(update=update_data)
    return race_repo.set(race_id, updated_race)


@race_router.delete("/{race_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(race_id: int, race_repo: RaceRepoDep, driver_in_race_repo: DriverInRaceRepoDep
                       ):
    race_repo.delete(race_id)
    registrations = driver_in_race_repo.get_all()
    for reg in registrations:
        if reg.race_id == race_id:
            driver_in_race_repo.delete(reg.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@race_router.get("/{race_id}/drivers", response_model=list[Driver], responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_all_drivers(
        race_id: int,
        driver_repo: DriverRepoDep,
        race_repo: RaceRepoDep,
        driver_in_race_repo: DriverInRaceRepoDep
) -> list[Driver]:
    race = get_race_or_404(race_id, race_repo)
    all_race_registrations = driver_in_race_repo.get_all()

    drivers: list[Driver] = []

    for reg in all_race_registrations:
        if reg.race_id == race.id:
            driver = driver_repo.get(reg.driver_id)
            if driver is not None:
                drivers.append(driver)

    return drivers


def _get_driver_in_race(race: Race, driver: Driver, driver_in_race_repo: DriverInRaceRepoDep) -> DriverInRace | None:
    registrations = driver_in_race_repo.get_all()
    target = [reg for reg in registrations if reg.race_id == race.id and reg.driver_id == driver.id]
    if len(target) == 0:
        return None
    return target[0]

@race_router.post("/{race_id}/drivers", status_code=status.HTTP_201_CREATED, response_model=DriverInRace, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
    status.HTTP_409_CONFLICT: {"model": "Driver already registered for this race"}
})
async def register_driver(
        race_id: int,
        body: DriverRegistration,
        driver_repo: DriverRepoDep,
        race_repo: RaceRepoDep,
        driver_in_race_repo: DriverInRaceRepoDep

) -> DriverInRace:
    driver = get_driver_or_404(body.driver_id, driver_repo)
    race = get_race_or_404(race_id, race_repo)

    registration = _get_driver_in_race(race, driver, driver_in_race_repo)
    if registration is not None:
        raise HTTPError(status.HTTP_409_CONFLICT, "Driver already registered for this race")

    driver_in_race = DriverInRace(driver_id=driver.id, race_id=race.id)
    return driver_in_race_repo.add(driver_in_race)



@race_router.delete("/{race_id}/drivers/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unregister_driver(
        race_id: int,
        driver_id: int,
        race_repo: RaceRepoDep,
        driver_in_race_repo: DriverInRaceRepoDep
):
    race = get_race_or_404(race_id, race_repo)
    registrations = driver_in_race_repo.get_all()
    target = [reg for reg in registrations if reg.race_id == race.id and reg.driver_id == driver_id]
    if len(target) > 0:
        driver_in_race_repo.delete(target[0].id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
