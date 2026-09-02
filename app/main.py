from fastapi import FastAPI

from app.routers import entity_2_router, entity_1_router

app = FastAPI()

app.include_router(entity_1_router)

app.include_router(entity_2_router)
