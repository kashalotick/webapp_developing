from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from app.schemas import Race, Driver, RegisteredDriver

race_router = APIRouter(prefix="/entity_2")


@race_router.post("/", response_model=list[Race])
async def create(body: Race):
    pass


@race_router.get("/", response_model=list[Race])
async def get_all():
    pass


@race_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all():
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@race_router.get("/{race_id}", response_model=Race, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_by_id(race_id: int):
    pass


@race_router.patch("/{race_id}", response_model=Race, responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def patch_by_id(race_id: int, body: Race):
    pass


@race_router.delete("/{race_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(race_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# NE CRUD
@race_router.get("/{race_id}/drivers", response_model=list[Driver], responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_all_races(race_id: int):
    pass

@race_router.post("/{race_id}/drivers", response_model=list[Driver], responses={
    status.HTTP_404_NOT_FOUND: {"model": "Not found"},
})
async def get_all_races(race_id: int, body: RegisteredDriver):
    pass
