class Promotion:
    def __init__(self, name: str, description: str, active: bool = False):
        self._name = name
        self._description = description
        self._active = active

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def is_active(self) -> bool:
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False
