from .Position import Position
from .OrganizationUnit import OrganizationUnit
from .EmploymentContract import EmploymentContract
from salary_system3.compensation.CompensationPackage import CompensationPackage

class Employee:
    def __init__(
        self,
        employee_id: int,
        full_name: str,
        employment_type: str,
        position: Position=None,
        organization_unit: OrganizationUnit=None,
        employment_contract: EmploymentContract=None,
        compensation_package: CompensationPackage=None,
        contact_info: dict | None = None
    ):
        self.id = employee_id
        self.full_name = full_name
        self.employment_type = employment_type

        self.position = position
        self.organization_unit = organization_unit
        self.employment_contract = employment_contract
        self.compensation_package = compensation_package

        self.contact_info = contact_info if contact_info else {}

    def get_profile(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "employment_type": self.employment_type,
            "contact_info": self.contact_info,
            "position": str(self.position) if self.position else None,
            "organization_unit": str(self.organization_unit) if self.organization_unit else None,
            "contract": str(self.employment_contract) if self.employment_contract else None,
            "compensation_package": str(self.compensation_package) if self.compensation_package else None,
        }

    def update_contact_info(self, new_contact_info: dict) -> None:
        if not isinstance(new_contact_info, dict):
            raise ValueError("new_contact_info must be a dict")

        self.contact_info.update(new_contact_info)

    def __repr__(self):
        return f"Employee(id={self.id}, full_name='{self.full_name}', employment_type='{self.employment_type}')"
