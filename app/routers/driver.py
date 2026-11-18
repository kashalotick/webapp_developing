from fastapi import APIRouter
from starlette import status

from app.exceptions import BusinessException, ErrorSchema
from app.schemas.driver import DriverCreate, DriverRead, DriverUpdate, RatingDelta
from app.schemas.race import RaceRead
from app.services.driver_repository import DriverRepoDep

driver_router = APIRouter(prefix="/drivers", tags=["Drivers"])


@driver_router.post("", status_code=status.HTTP_201_CREATED, response_model=DriverRead)
async def create(body: DriverCreate, driver_repo: DriverRepoDep) -> DriverRead:
    return await driver_repo.add(body)


@driver_router.get("", response_model=list[DriverRead])
async def get_all(driver_repo: DriverRepoDep) -> list[DriverRead]:
    return await driver_repo.get_all()


@driver_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all(driver_repo: DriverRepoDep):
    await driver_repo.clear()
    return None


@driver_router.get("/{driver_id}", response_model=DriverRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found", "model": ErrorSchema},
})
async def get_by_id(driver_id: int, driver_repo: DriverRepoDep) -> DriverRead:
    result = await driver_repo.get(driver_id)
    if result is None:
        raise BusinessException.not_found(DriverRead)
    return result

@driver_router.patch("/{driver_id}", response_model=DriverRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found", "model": ErrorSchema},
})
async def patch_by_id(driver_id: int, body: DriverUpdate, driver_repo: DriverRepoDep) -> DriverRead:
    result = await driver_repo.patch(driver_id, body)
    if result is None:
        raise BusinessException.not_found(DriverRead)
    return result


@driver_router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found", "model": ErrorSchema},
})
async def delete_by_id(driver_id: int, driver_repo: DriverRepoDep):
    result = await driver_repo.delete(driver_id)
    if not result:
        raise BusinessException.not_found(DriverRead)
    return None


@driver_router.get("/{driver_id}/races", response_model=list[RaceRead], responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found", "model": ErrorSchema},
})
async def get_all_races(
        driver_id: int,
        driver_repo: DriverRepoDep
) -> list[RaceRead]:
    return await driver_repo.get_driver_races(driver_id)


@driver_router.post("/{driver_id}/rating/change", response_model=DriverRead, responses={
    status.HTTP_404_NOT_FOUND: {"description": "Not found", "model": ErrorSchema},
})
async def change_rating(
        driver_id: int,
        body: RatingDelta,
        driver_repo: DriverRepoDep
) -> DriverRead:
    result = await driver_repo.change_rating(driver_id, body.delta)
    if result is None:
        raise BusinessException.not_found(DriverRead)
    return result
