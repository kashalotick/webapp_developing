from fastapi import APIRouter

from app.responsedoc import ResponseDoc
from app.security import create_token
from app.schemas.user import AccessTokenRead, UserPost
from app.services.user_repository import UserRepoDep

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])




@auth_router.post("/login", response_model=AccessTokenRead, responses=ResponseDoc().not_authorized_401().get_dict())
async def login(cred: UserPost, user_repo: UserRepoDep) -> AccessTokenRead:
    user = await user_repo.login(cred)
    return AccessTokenRead(token=create_token(user))


@auth_router.post("/register", response_model=AccessTokenRead, responses=ResponseDoc().not_authorized_401().get_dict())
async def register(cred: UserPost, user_repo: UserRepoDep) -> AccessTokenRead:
    await user_repo.register(cred)
    user = await user_repo.login(cred)
    return AccessTokenRead(token=create_token(user))
