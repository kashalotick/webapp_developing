import logging
from typing import Annotated

from fastapi import Depends
from starlette.requests import Request

from app.api_config import ApiConfigDep
from app.exceptions import BusinessException, ErrorCode


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)

LoggerDep = Annotated[logging.Logger, Depends(get_logger)]



SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
async def forbid_writes_if_read_only(request: Request, config: ApiConfigDep):
    if config.readonly and request.method not in SAFE_METHODS:
        raise BusinessException.from_code(ErrorCode.READ_ONLY_MODE)