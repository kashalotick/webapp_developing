from typing import Generic, TypeVar

from pydantic import BaseModel

from app.schemas import Driver, Race, DriverInRace

T = TypeVar("T", bound=BaseModel)


class InMemoryRepository(Generic[T]):
    def __init__(self) -> None:
        self.storage: dict[int, T] = {}
        self.next_id: int = 0

    def get_next_id(self) -> int:
        self.next_id += 1
        return self.next_id

    def add(self, entity: T) -> T:
        entity_id = self.get_next_id()
        entity.id = entity_id
        self.storage[entity_id] = entity
        return entity

    def get(self, entity_id: int) -> T | None:
        return self.storage.get(entity_id)

    def get_all(self) -> list[T]:
        return list(self.storage.values())

    def set(self, entity_id: int, entity: T) -> T:
        entity.id = entity_id
        self.storage[entity_id] = entity
        if entity_id > self.next_id:
            self.next_id = entity_id
        return entity

    def delete(self, entity_id: int) -> None:
        self.storage.pop(entity_id, None)


class DriverRepository(InMemoryRepository[Driver]):
    pass


class RaceRepository(InMemoryRepository[Race]):
    pass


class DriverInRaceRepository(InMemoryRepository[DriverInRace]):
    pass
