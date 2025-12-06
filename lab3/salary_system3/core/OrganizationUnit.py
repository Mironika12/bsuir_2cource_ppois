class OrganizationUnit:
    def __init__(self, unit_id: int, name: str, manager_id: int | None = None):
        self.id = unit_id
        self.name = name
        self.manager_id = manager_id
        self.members = []

    def add_member(self, employee_id: int) -> None:
        if employee_id not in self.members:
            self.members.append(employee_id)

    def remove_member(self, employee_id: int) -> None:
        if employee_id in self.members:
            self.members.remove(employee_id)

    def __repr__(self):
        return f"OrganizationUnit(id={self.id}, name='{self.name}', manager_id={self.manager_id})"
