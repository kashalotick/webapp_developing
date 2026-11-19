import enum
from typing import Type

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    code: str
    message: str


class ErrorCode(enum.Enum):
    DRIVER_ALREADY_REGISTERED = "Driver is already registered in race"
    DRIVER_IS_NOT_REGISTERED = "Driver is not registered in race"
    NOT_FOUND = "Not found"
    READ_ONLY_MODE = "Read only mode"
    INVALID_CREDENTIALS = "Invalid credentials"
    NOT_AUTHENTICATED = "Not authenticated"
    INVALID_TOKEN = "Invalid token"


error_status_code_map: dict[ErrorCode, int] = {
    ErrorCode.DRIVER_ALREADY_REGISTERED: 409,
    ErrorCode.DRIVER_IS_NOT_REGISTERED: 404,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.READ_ONLY_MODE: 405,
    ErrorCode.INVALID_CREDENTIALS: 401,
    ErrorCode.NOT_AUTHENTICATED: 401,
    ErrorCode.INVALID_TOKEN: 401,

}


class BusinessException(Exception):
    def __init__(self, error_code: ErrorCode, message: str | None = None):
        self.error_code = error_code
        self.message = error_code.value if message is None else message
        super().__init__(self.message)

    @classmethod
    def from_code(cls, error_code: ErrorCode):
        return cls(error_code)

    @classmethod
    def not_found(cls, entity: Type):
        message = f"{ErrorCode.NOT_FOUND.value}: {entity.__name__}"
        return cls(ErrorCode.NOT_FOUND, message)
