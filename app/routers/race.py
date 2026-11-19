from typing import Annotated

from fastapi import APIRouter, Query
from starlette import status

from app.cache import CacheDep
from app.exceptions import BusinessException, ErrorSchema
from app.responsedoc import ResponseDoc
from app.schemas.driver import DriverRead, DriverInRace
from app.schemas.race import RaceRead, RaceCreate, RaceUpdate, DriverRegistration
from app.security import CurrentUserDep
from app.services.race_repository import RaceRepoDep

race_router = APIRouter(prefix="/api/races", tags=["Races"])


@race_router.post("", status_code=status.HTTP_201_CREATED, response_model=RaceRead, dependencies=[CurrentUserDep],
                  responses=ResponseDoc().not_authorized_401().method_not_allowed_405().get_dict())
async def create(body: RaceCreate, race_repo: RaceRepoDep) -> RaceRead:
    return await race_repo.add(body)


@race_router.get("", response_model=list[RaceRead])
async def get_all(race_repo: RaceRepoDep, cache: CacheDep, page: Annotated[int, Query(ge=1)] = 1) -> list[RaceRead]:
    c_data = cache.get(f"races_page{page}")
    if c_data:
        return c_data
    res = await race_repo.get_all(page)
    cache.set(f"races_page{page}", res)
    return res


@race_router.delete("", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CurrentUserDep], responses=ResponseDoc()
                    .not_authorized_401()
                    .method_not_allowed_405()
                    .get_dict(), )
async def delete_all(race_repo: RaceRepoDep) -> None:
    await race_repo.clear()
    return None


@race_router.get("/{race_id}", response_model=RaceRead, responses=ResponseDoc()
                 .not_found_404()
                 .get_dict())
async def get_by_id(race_id: int, race_repo: RaceRepoDep) -> RaceRead:
    result = await race_repo.get(race_id)
    if result is None:
        raise BusinessException.not_found(RaceRead)
    return result


@race_router.patch("/{race_id}", response_model=RaceRead, responses=ResponseDoc()
                   .not_found_404()
                   .not_authorized_401()
                   .method_not_allowed_405()
                   .get_dict(), dependencies=[CurrentUserDep])
async def patch_by_id(race_id: int, body: RaceUpdate, race_repo: RaceRepoDep) -> RaceRead:
    result = await race_repo.patch(race_id, body)
    if result is None:
        raise BusinessException.not_found(RaceRead)
    return result


@race_router.delete("/{race_id}", status_code=status.HTTP_204_NO_CONTENT, responses=ResponseDoc()
                    .not_found_404()
                    .not_authorized_401()
                    .method_not_allowed_405()
                    .get_dict(), dependencies=[CurrentUserDep])
async def delete_by_id(race_id: int, race_repo: RaceRepoDep) -> None:
    result = await race_repo.delete(race_id)
    if not result:
        raise BusinessException.not_found(RaceRead)
    return None


@race_router.get("/{race_id}/drivers", response_model=list[DriverRead], responses=ResponseDoc()
                 .not_found_404()
                 .get_dict(), )
async def get_all_drivers(
        race_repo: RaceRepoDep,
        cache: CacheDep,
        race_id: int,
        page: Annotated[int, Query(ge=1)] = 1
) -> list[DriverRead]:
    c_data = cache.get(f"races_{race_id}_drivers_page{page}")
    if c_data:
        return c_data
    res = await race_repo.get_drivers_in_race(race_id, page)
    cache.set(f"races_{race_id}_drivers_page{page}", res)
    return res


@race_router.post("/{race_id}/drivers", status_code=status.HTTP_201_CREATED, response_model=DriverInRace,
                  responses=ResponseDoc()
                  .not_found_404()
                  .not_authorized_401()
                  .conflict_409()
                  .method_not_allowed_405()
                  .get_dict(), dependencies=[CurrentUserDep])
async def register_driver(
        race_id: int,
        body: DriverRegistration,
        race_repo: RaceRepoDep,

) -> DriverInRace:
    return await race_repo.register_driver(race_id, body.driver_id)


@race_router.delete("/{race_id}/drivers/{driver_id}", status_code=status.HTTP_204_NO_CONTENT, responses=ResponseDoc()
                    .not_found_404()
                    .not_authorized_401()
                    .method_not_allowed_405()
                    .get_dict(), dependencies=[CurrentUserDep])
async def unregister_driver(
        race_id: int,
        driver_id: int,
        race_repo: RaceRepoDep,
) -> None:
    await race_repo.unregister_driver(race_id, driver_id)
    return None
