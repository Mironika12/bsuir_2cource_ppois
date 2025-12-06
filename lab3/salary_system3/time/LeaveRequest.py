from salary_system3.core.Employee import Employee

class LeaveRequest:
    def __init__(self, request_id: str, employee: 'Employee', leave_type: str):
        self.request_id: str = request_id
        self.employee: 'Employee' = employee
        self.leave_type: str = leave_type
        self.approved: bool = False
        self.rejected: bool = False

    def approve(self) -> None:
        self.approved = True
        self.rejected = False

    def reject(self) -> None:
        self.approved = False
        self.rejected = True
