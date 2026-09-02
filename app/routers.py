from fastapi import APIRouter

entity_1_router = APIRouter(prefix="/entity_1")


@entity_1_router.post("/")
async def create():
    pass


@entity_1_router.get("/")
async def get_all():
    pass


@entity_1_router.delete("/")
async def delete_all():
    pass


@entity_1_router.get("/{entity_id}")
async def get_by_id(entity_id: int):
    pass


@entity_1_router.patch("/{entity_id}")
async def patch_by_id(entity_id: int):
    pass


@entity_1_router.delete("/{entity_id}")
async def delete_by_id(entity_id: int):
    pass


entity_2_router = APIRouter(prefix="/entity_2")
