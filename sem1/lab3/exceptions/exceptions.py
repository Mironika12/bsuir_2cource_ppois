class EmployeeNotFoundException(Exception):
    """Исключение при отсутствии сотрудника"""
    pass

class InsufficientFundsException(Exception):
    """Исключение при недостатке средств"""
    pass

class InvalidContractException(Exception):
    """Исключение при недействительном контракте"""
    pass

class PayrollProcessingException(Exception):
    """Исключение при обработке payroll"""
    pass

class TaxFilingException(Exception):
    """Исключение при налоговом оформлении"""
    pass

class PaymentGatewayException(Exception):
    """Исключение при ошибке платежного шлюза"""
    pass

class ValidationException(Exception):
    """Исключение при ошибке валидации"""
    pass

class DuplicateRecordException(Exception):
    """Исключение при дублировании записи"""
    pass

class UnauthorizedAccessException(Exception):
    """Исключение при несанкционированном доступе"""
    pass

class DataIntegrityException(Exception):
    """Исключение при нарушении целостности данных"""
    pass

class UnsupportedCurrencyException(Exception):
    """Исключение при неподдерживаемой валюте"""
    pass

class TimesheetLockedException(Exception):
    """Исключение при заблокированном таймшите"""
    pass
