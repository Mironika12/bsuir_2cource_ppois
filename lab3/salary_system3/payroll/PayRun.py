from typing import List
from .PayrollRecord import PayrollRecord
from salary_system3.payments.PaymentBatch import PaymentBatch
from exceptions.exceptions import (
    ValidationException, 
    DuplicateRecordException, 
    EmployeeNotFoundException, 
    InsufficientFundsException, 
    PayrollProcessingException,
    DataIntegrityException,
    InvalidContractException, 
    UnsupportedCurrencyException, 
    UnauthorizedAccessException, 
    PaymentGatewayException,
    TimesheetLockedException,
    TaxFilingException
    )

class PayRun:
    def __init__(self, pay_run_id: str, period_start: str, period_end: str,
                 payroll_records: List["PayrollRecord"], payment_batches: List["PaymentBatch"]):
        self.pay_run_id: str = pay_run_id
        self.period_start: str = period_start
        self.period_end: str = period_end
        self.payroll_records: List["PayrollRecord"] = payroll_records
        self.payment_batches: List["PaymentBatch"] = payment_batches
        self.status: str = "pending" 
        self.total_amount: float = 0.0
        self.processed_records: List[str] = []

    def validate_payrun(self) -> bool:
        try:
            if not self.payroll_records:
                raise ValidationException("Нет записей payroll для обработки")
            
            if self.pay_run_id in self.processed_records:
                raise DuplicateRecordException(f"PayRun с ID {self.pay_run_id} уже был обработан")
            
            if self.period_start >= self.period_end:
                raise ValidationException(f"Дата начала {self.period_start} должна быть раньше даты окончания {self.period_end}")
            
            for record in self.payroll_records:
                if not hasattr(record, 'employee_id') or not record.employee_id:
                    raise EmployeeNotFoundException(f"Не найден сотрудник в записи {record.record_id}")
                
                if record.net_pay <= 0:
                    raise InsufficientFundsException(f"Некорректная сумма выплаты: {record.net_pay}")
                    
            return True
            
        except (ValidationException, EmployeeNotFoundException, 
                InsufficientFundsException, DuplicateRecordException) as e:
            raise PayrollProcessingException(f"Ошибка валидации PayRun: {str(e)}")

    def calculate_total_payout(self) -> float:
        """Расчет общей суммы выплат для PayRun"""
        try:
            total = 0.0
            
            for record in self.payroll_records:
                if not hasattr(record, 'net_pay'):
                    raise DataIntegrityException(f"Запись {record.record_id} не содержит net_pay")
                
                if hasattr(record, 'employee') and hasattr(record.employee, 'employment_contract'):
                    contract = record.employee.employment_contract
                    if contract and not contract.is_active():
                        raise InvalidContractException(f"Контракт сотрудника {record.employee_id} не активен")
                
                if record.net_pay > 1000000:
                    raise UnsupportedCurrencyException(f"Подозрительная сумма выплаты: {record.net_pay}")
                
                total += record.net_pay
            
            self.total_amount = total
            return total
            
        except (DataIntegrityException, InvalidContractException, 
                UnsupportedCurrencyException) as e:
            raise PayrollProcessingException(f"Ошибка расчета выплат: {str(e)}")

    def execute(self) -> bool:
        """Выполнение PayRun с обработкой всех платежей"""
        try:
            if self.status != "pending":
                raise UnauthorizedAccessException("PayRun уже обрабатывается или завершен")
            
            self.validate_payrun()

            total = self.calculate_total_payout()

            if total > 50000:
                tax_result = self._file_taxes()
                if not tax_result:
                    raise TaxFilingException("Ошибка отправки налоговой отчетности")

            payment_success = self._process_payments()
            if not payment_success:
                raise PaymentGatewayException("Ошибка обработки платежей через платежный шлюз")
            
            if not self._check_timesheets():
                raise TimesheetLockedException("Некоторые таймшиты заблокированы или не заполнены")
            
            self.status = "completed"
            self.processed_records.append(self.pay_run_id)
            
            print(f"PayRun {self.pay_run_id} успешно выполнен. Общая сумма: {total}")
            return True
            
        except Exception as e:
            self.status = "failed"
            raise PayrollProcessingException(f"Ошибка выполнения PayRun: {str(e)}")

    def rollback(self) -> bool:
        """Отмена выполненного PayRun"""
        try:
            if self.status != "completed":
                raise ValidationException("Можно отменить только завершенный PayRun")
            
            if self.total_amount > 100000:
                raise UnauthorizedAccessException("Требуется дополнительная авторизация для отмены крупного PayRun")
            
            for batch in self.payment_batches:
                if not batch.submit_batch():
                    raise PaymentGatewayException(f"Ошибка отмены batch {batch.batch_id}")
            
            self.status = "rolled_back"
            self.total_amount = 0.0
            
            if self.pay_run_id in self.processed_records:
                self.processed_records.remove(self.pay_run_id)
            
            print(f"PayRun {self.pay_run_id} отменен")
            return True
            
        except Exception as e:
            raise PayrollProcessingException(f"Ошибка отмены PayRun: {str(e)}")

    def _file_taxes(self) -> bool:
        return True

    def _process_payments(self) -> bool:
        try:
            for batch in self.payment_batches:
                if not batch.compile():
                    return False
                if not batch.submit_batch():
                    return False
            return True
        except:
            return False

    def _check_timesheets(self) -> bool:
        return len(self.payroll_records) > 0

    def __repr__(self):
        return f"PayRun(id={self.pay_run_id}, status={self.status}, total={self.total_amount})"