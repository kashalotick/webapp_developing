from abc import ABC, abstractmethod
from typing import Annotated

import bcrypt
from fastapi import Depends
from sqlalchemy import select

from app.exceptions import BusinessException, ErrorCode
from app.models.user_model import UserModel
from app.schemas.user import UserPost, UserRead
from app.services.repository import AbstractAsyncRepository, AsyncRepository


class AbstractUserRepository(AbstractAsyncRepository[UserModel, UserPost, UserPost, UserRead], ABC):
    @abstractmethod
    async def register(self, cred: UserPost) -> UserRead:
        pass

    @abstractmethod
    async def login(self, cred: UserPost) -> UserRead:
        pass


class UserRepository(AbstractUserRepository, AsyncRepository):

    async def register(self, cred: UserPost) -> UserRead:
        hashed_password = bcrypt.hashpw(cred.password.encode(), bcrypt.gensalt())
        user = UserModel(login=cred.login, password_hash=hashed_password.decode())
        return await self.add(user)

    async def login(self, cred: UserPost) -> UserRead:
        query = select(UserModel).where(UserModel.login == cred.login)
        result = await self.db.scalar(query)
        if not result:
            raise BusinessException.from_code(ErrorCode.INVALID_CREDENTIALS)

        if bcrypt.checkpw(cred.password.encode(), result.password_hash.encode()):
            return UserRead.model_validate(result)

        raise BusinessException.from_code(ErrorCode.INVALID_CREDENTIALS)


UserRepoDep = Annotated[AbstractUserRepository, Depends(UserRepository)]
