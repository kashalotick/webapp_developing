import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db import Base, engine
from app.models import *  # noqa
from app.exceptions import BusinessException, error_status_code_map, ErrorSchema
from app.routers.driver import driver_router
from app.routers.race import race_router

from app.deps import get_logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logging.getLogger("uvicorn.access").disabled = True
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(driver_router)
app.include_router(race_router)

logger = get_logger()


@app.exception_handler(BusinessException)
async def business_exception_handler(
        request: Request,
        exc: BusinessException,
) -> JSONResponse:
    status_code = error_status_code_map[exc.error_code]
    logger.warning(
        "%s %s -> %d %s: %s",
        request.method, request.url.path, status_code, exc.error_code.name, exc.message,
    )
    return JSONResponse(
        status_code=error_status_code_map[exc.error_code],
        content=ErrorSchema(code=exc.error_code.name, message=exc.message).model_dump(),
    )
