import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_config import ApiConfig

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
class AbstractAsyncRepository(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]):

    @abstractmethod
    async def add(self, schema: CreateSchemaType) -> ReadSchemaType:
        pass
    @abstractmethod
    async def get(self, entity_id: int) -> ReadSchemaType | None:
        pass
    @abstractmethod
    async def get_all(self, page: int) -> list[ReadSchemaType]:
        pass

    @abstractmethod
    async def patch(self, entity_id: int, schema: UpdateSchemaType) -> ReadSchemaType | None:
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        pass
    @abstractmethod
    async def clear(self) -> bool:
        pass



class AsyncRepository(
    AbstractAsyncRepository[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]
):
    def __init__(
            self,
            db: AsyncSession,
            model: Type[ModelType],
            read_schema: Type[ReadSchemaType],
            logger: logging.Logger,
            api_config: ApiConfig,
    ) -> None:
        self.db = db
        self.model = model
        self.read_schema = read_schema
        self.logger = logger.getChild(type(self).__name__)
        self.api_config = api_config


    def page(self, page: int) -> tuple[int, int]:
        limit = self.api_config.page_size
        offset = (page - 1) * limit
        return limit, offset

    async def add(self, schema: CreateSchemaType) -> ReadSchemaType:
        db_entity = self.model(**schema.model_dump())
        self.db.add(db_entity)
        await self.db.flush()
        await self.db.refresh(db_entity)
        self.logger.info(f"Added entity with id {db_entity.id}")
        return self.read_schema.model_validate(db_entity)

    async def get(self, entity_id: int) -> ReadSchemaType | None:
        db_entity = await self.db.get(self.model, entity_id)
        if not db_entity:
            return None
        return self.read_schema.model_validate(db_entity)

    async def get_all(self, page: int) -> list[ReadSchemaType]:
        limit, offset = self.page(page)
        query = select(self.model).limit(limit).offset(offset)
        result = await self.db.scalars(query)
        return [self.read_schema.model_validate(item) for item in result.all()]

    async def patch(self, entity_id: int, schema: UpdateSchemaType) -> ReadSchemaType | None:
        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get(entity_id)

        query = (
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await self.db.scalar(query)
        await self.db.flush()

        if not result:
            self.logger.warning(f"Entity with id {entity_id} not found")
            return None
        self.logger.info(f"Updated entity with id {entity_id}")
        return self.read_schema.model_validate(result)

    async def delete(self, entity_id: int) -> bool:
        query = delete(self.model).where(self.model.id == entity_id).returning(self.model.id)
        result = await self.db.scalar(query)
        await self.db.flush()
        self.logger.info(f"Deleted entity with id {entity_id}")
        return result is not None
    async def clear(self) -> bool:
        query = delete(self.model).returning(self.model.id)
        result = await self.db.execute(query)
        await self.db.flush()
        self.logger.info("Cleared all entities")
        return len(result.all()) > 0



    


