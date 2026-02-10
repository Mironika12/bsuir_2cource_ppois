from typing import Any, Dict


class Repository:
    def __init__(self, repo_id: str, data_source: Any, cache: Dict[str, Any] | None = None):
        self.repo_id: str = repo_id
        self.data_source: Any = data_source
        self.cache: Dict[str, Any] = cache if cache is not None else {}

    def save(self, entity: Any) -> bool:
        entity_id = getattr(entity, "id", None) or getattr(entity, "employee_id", None)
        if entity_id is None:
            return False
        self.data_source[entity_id] = entity
        self.cache[entity_id] = entity
        return True

    def find_by_id(self, entity_id: str) -> Any | None:
        if entity_id in self.cache:
            return self.cache[entity_id]
        entity = self.data_source.get(entity_id)
        if entity:
            self.cache[entity_id] = entity
        return entity
