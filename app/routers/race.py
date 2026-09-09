from fastapi import APIRouter
from starlette import status

from app.deps import RaceRepoDep
from app.exceptions import BusinessException, ErrorSchema
from app.schemas.driver import DriverRead, DriverInRace
from app.schemas.race import RaceRead, RaceCreate, RaceUpdate, DriverRegistration

race_router = APIRouter(prefix="/races", tags=["Races"])


@race_router.post("", status_code=status.HTTP_201_CREATED, response_model=RaceRead)
async def create(body: RaceCreate, race_repo: RaceRepoDep) -> RaceRead:
    return await race_repo.add(body)


@race_router.get("", response_model=list[RaceRead])
async def get_all(race_repo: RaceRepoDep) -> list[RaceRead]:
    return await race_repo.get_all()


@race_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(race_repo: RaceRepoDep) -> None:
    await race_repo.clear()
    return None


@race_router.get("/{race_id}", response_model=RaceRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found",  "model": ErrorSchema},
})
async def get_by_id(race_id: int, race_repo: RaceRepoDep) -> RaceRead:
    result = await race_repo.get(race_id)
    if result is None:
        raise BusinessException.not_found(RaceRead)
    return result


@race_router.patch("/{race_id}", response_model=RaceRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found",  "model": ErrorSchema},
})
async def patch_by_id(race_id: int, body: RaceUpdate, race_repo: RaceRepoDep) -> RaceRead:
    result = await race_repo.patch(race_id, body)
    if result is None:
        raise BusinessException.not_found(RaceRead)
    return result


@race_router.delete("/{race_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found", "model": ErrorSchema},
})
async def delete_by_id(race_id: int, race_repo: RaceRepoDep) -> None:
    result = await race_repo.delete(race_id)
    if not result:
        raise BusinessException.not_found(RaceRead)
    return None


@race_router.get("/{race_id}/drivers", response_model=list[DriverRead], responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found",  "model": ErrorSchema},
})
async def get_all_drivers(
        race_id: int,
        race_repo: RaceRepoDep,
) -> list[DriverRead]:
    return await race_repo.get_drivers_in_race(race_id)


@race_router.post("/{race_id}/drivers", status_code=status.HTTP_201_CREATED, response_model=DriverInRace, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found",  "model": ErrorSchema},
    status.HTTP_409_CONFLICT: {"description": "Driver already registered for this race",  "model": ErrorSchema}
})
async def register_driver(
        race_id: int,
        body: DriverRegistration,
        race_repo: RaceRepoDep

) -> DriverInRace:
    return await race_repo.register_driver(race_id, body.driver_id)


@race_router.delete("/{race_id}/drivers/{driver_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found",  "model": ErrorSchema},
})
async def unregister_driver(
        race_id: int,
        driver_id: int,
        race_repo: RaceRepoDep
) -> None:
    await race_repo.unregister_driver(race_id, driver_id)
    return None
