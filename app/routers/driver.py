from typing import Annotated

from fastapi import APIRouter, Query
from starlette import status

from app.cache import CacheDep
from app.exceptions import BusinessException, ErrorSchema
from app.responsedoc import ResponseDoc
from app.schemas.driver import DriverCreate, DriverRead, DriverUpdate, RatingDelta
from app.schemas.race import RaceRead
from app.security import CurrentUserDep
from app.services.driver_repository import DriverRepoDep

driver_router = APIRouter(prefix="/api/drivers", tags=["Drivers"])


@driver_router.post("", status_code=status.HTTP_201_CREATED, response_model=DriverRead, dependencies=[CurrentUserDep],
                    responses=ResponseDoc().not_authorized_401().method_not_allowed_405().get_dict())
async def create(body: DriverCreate, driver_repo: DriverRepoDep) -> DriverRead:
    return await driver_repo.add(body)


@driver_router.get("", response_model=list[DriverRead])
async def get_all(driver_repo: DriverRepoDep, cache: CacheDep, page: Annotated[int, Query(ge=1)] = 1) -> list[
    DriverRead]:
    c_data = cache.get(f"drivers_page{page}")
    if c_data:
        return c_data
    res = await driver_repo.get_all(page)
    cache.set(f"drivers_page{page}", res)
    return res


@driver_router.delete("", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CurrentUserDep],
                      responses=ResponseDoc().not_authorized_401().method_not_allowed_405().get_dict(), )
async def delete_all(driver_repo: DriverRepoDep):
    await driver_repo.clear()
    return None


@driver_router.get("/{driver_id}", response_model=DriverRead, responses=ResponseDoc()
                   .not_found_404()
                   .not_authorized_401()
                   .get_dict(), )
async def get_by_id(driver_id: int, driver_repo: DriverRepoDep) -> DriverRead:
    result = await driver_repo.get(driver_id)
    if result is None:
        raise BusinessException.not_found(DriverRead)
    return result


@driver_router.patch("/{driver_id}", response_model=DriverRead, responses=ResponseDoc()
                     .not_found_404()
                     .not_authorized_401()
                     .method_not_allowed_405()
                     .get_dict(), dependencies=[CurrentUserDep])
async def patch_by_id(driver_id: int, body: DriverUpdate, driver_repo: DriverRepoDep) -> DriverRead:
    result = await driver_repo.patch(driver_id, body)
    if result is None:
        raise BusinessException.not_found(DriverRead)
    return result


@driver_router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT, responses=ResponseDoc()
                      .not_found_404()
                      .not_authorized_401()
                      .method_not_allowed_405()
                      .get_dict(), dependencies=[CurrentUserDep])
async def delete_by_id(driver_id: int, driver_repo: DriverRepoDep):
    result = await driver_repo.delete(driver_id)
    if not result:
        raise BusinessException.not_found(DriverRead)
    return None


@driver_router.get("/{driver_id}/races", response_model=list[RaceRead], responses=ResponseDoc()
                   .not_found_404()
                   .get_dict())
async def get_all_races(
        driver_repo: DriverRepoDep,
        cache: CacheDep,
        driver_id: int,
        page: Annotated[int, Query(ge=1)] = 1
) -> list[RaceRead]:
    c_data = cache.get(f"drivers_{driver_id}_races_page{page}")
    if c_data:
        return c_data
    res = await driver_repo.get_driver_races(driver_id, page)
    cache.set(f"drivers_{driver_id}_races_page{page}", res)
    return res


@driver_router.post(
    "/{driver_id}/rating/change",
    response_model=DriverRead,
    responses=ResponseDoc()
    .not_found_404()
    .not_authorized_401()
    .method_not_allowed_405()
    .get_dict(),
    dependencies=[CurrentUserDep])
async def change_rating(
        driver_id: int,
        body: RatingDelta,
        driver_repo: DriverRepoDep
) -> DriverRead:
    result = await driver_repo.change_rating(driver_id, body.delta)
    if result is None:
        raise BusinessException.not_found(DriverRead)
    return result
