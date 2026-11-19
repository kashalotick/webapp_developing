from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.responses import Response

from app.config import Settings, settings
from app.exceptions import BusinessException, ErrorCode
from app.schemas.user import UserPost, UserRead
from app.services.user_repository import UserRepoDep

bearer = HTTPBearer(auto_error=False)

def create_token(c: UserRead) -> str:
    token = jwt.encode(
        {"sub": c.login, "exp": datetime.now(timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)},
        settings.JWT_SECRET,
        algorithm='HS256',
    )
    return token


def current_user(cred: HTTPAuthorizationCredentials | None = Depends(bearer)) -> str:
    if not cred:
        raise BusinessException.from_code(ErrorCode.NOT_AUTHENTICATED)
    try:
        return jwt.decode(cred.credentials, settings.JWT_SECRET, algorithms=['HS256'])["sub"]
    except jwt.PyJWTError:
        raise BusinessException.from_code(ErrorCode.INVALID_TOKEN)

CurrentUserDep = Annotated[str, Depends(current_user)]