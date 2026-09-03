from pathlib import Path
from typing import Any
from pydantic import BaseModel, TypeAdapter

from app.services.repository import InMemoryRepository


class RepositorySerializer:
    def __init__(self, base_dir: str | Path = "./data") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.entries: list[tuple[InMemoryRepository[Any], type[BaseModel]]] = []

    def register(self, repo: InMemoryRepository[Any], model_cls: type[BaseModel]) -> None:
        self.entries.append((repo, model_cls))

    def _get_file_path(self, repo: InMemoryRepository[Any]) -> Path:
        return self.base_dir / f"{repo.__class__.__name__}.json"

    def serialize(self) -> None:
        for repo, model_cls in self.entries:
            file_path = self._get_file_path(repo)
            adapter = TypeAdapter(dict[int, model_cls])
            with open(file_path, "wb") as f:
                f.write(adapter.dump_json(repo.storage, indent=2))

    def deserialize(self) -> None:
        for repo, model_cls in self.entries:
            file_path = self._get_file_path(repo)
            if not file_path.exists():
                continue

            with open(file_path, "rb") as f:
                data = f.read()

            adapter = TypeAdapter(dict[int, model_cls])
            repo.storage = adapter.validate_json(data)
            if repo.storage:
                repo.next_id = max(repo.storage.keys())