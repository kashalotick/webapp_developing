import logging
from typing import Annotated

from fastapi import Depends


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)

LoggerDep = Annotated[logging.Logger, Depends(get_logger)]



