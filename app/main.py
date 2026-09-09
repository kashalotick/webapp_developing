from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db import Base, engine
from app.models import * #noqa
from app.exceptions import BusinessException, error_status_code_map, ErrorSchema
from app.routers.driver import driver_router
from app.routers.race import race_router

REPOSITORY_PATH = Path.cwd() / "data"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(driver_router)
app.include_router(race_router)


@app.exception_handler(BusinessException)
async def business_exception_handler(
        request: Request,
        exc: BusinessException,
) -> JSONResponse:
    return JSONResponse(
        status_code=error_status_code_map[exc.error_code],
        content=ErrorSchema(code=exc.error_code.name, message=exc.message)
    )
