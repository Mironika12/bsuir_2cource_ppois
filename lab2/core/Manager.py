from Employee import Employee
from business.Coupon import Coupon
from exceptions.exceptions import (
    InvalidCouponException,
    SelfActionException,
)

class Manager(Employee):
    def approve_discount(self, coupon: Coupon):
        """
        Менеджер утверждает скидку по купону.
        """
        if not coupon.is_active():
            raise InvalidCouponException(coupon.get_code())

        return f"Менеджер {self.get_name()} одобрил купон {coupon.get_code()}."

    def fire_employee(self, employee: Employee):
        """
        Увольнение сотрудника (символическое действие).
        """
        if employee.get_employee_id() == self.get_employee_id():
            raise SelfActionException("уволить самого себя")

        return (
            f"Менеджер {self.get_name()} уволил сотрудника {employee.get_name()} "
            f"(ID: {employee.get_employee_id()})."
        )
