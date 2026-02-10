class RecruitmentRecord:
    def __init__(self, recruit_id: str, candidate_name: str, status: str):
        self.recruit_id: str = recruit_id
        self.candidate_name: str = candidate_name
        self.status: str = status
        self.converted_employee_id: str | None = None

    def convert_to_employee(self, employee_id: str) -> str:
        self.converted_employee_id = employee_id
        self.status = "converted"
        return self.converted_employee_id

    def archive(self) -> bool:
        self.status = "archived"
        return True
