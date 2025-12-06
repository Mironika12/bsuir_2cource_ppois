from typing import Dict, Any


class ConfigService:
    def __init__(self, config_id: str, values: Dict[str, Any], version: int):
        self.config_id: str = config_id
        self.values: Dict[str, Any] = values
        self.version: int = version

    def get(self, key: str) -> Any:
        return self.values.get(key)

    def set(self, key: str, value: Any) -> None:
        self.values[key] = value
        self.version += 1
