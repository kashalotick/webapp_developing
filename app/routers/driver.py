from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.schemas import Driver, RatingDelta, Race

driver_router = APIRouter(prefix="/entity_1")


# CRUD
@driver_router.post("/", response_model=list[Driver])
async def create(body: Driver):
    pass


@driver_router.get("/", response_model=list[Driver])
async def get_all():
    pass


@driver_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all():
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@driver_router.get("/{driver_id}", response_model=Driver, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_by_id(driver_id: int):
    pass


@driver_router.patch("/{driver_id}", response_model=Driver, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def patch_by_id(driver_id: int, body: Driver):
    pass


@driver_router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(driver_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# NE CRUD
@driver_router.get("/{driver_id}/races", response_model=Driver, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_all_races(driver_id: int):
    pass

@driver_router.post("/{driver_id}/rating/change", response_model=list[Race], responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def change_rating(driver_id: int, body: RatingDelta):
    pass