# Проект: Система управления заработной платой (salary_system3)

## Список классов, полей, методов и ассоциаций

### exceptions (12 классов, 0 полей, 0 методов)
EmployeeNotFoundException →  
InsufficientFundsException →  
InvalidContractException →  
PayrollProcessingException →  
TaxFilingException →  
PaymentGatewayException →  
ValidationException →  
DuplicateRecordException →  
UnauthorizedAccessException →  
DataIntegrityException →  
UnsupportedCurrencyException →  
TimesheetLockedException →  

### compensation (5 классов, 12 полей, 12 методов)
AllowanceComponent 3 3 →  
BaseSalaryComponent 3 4 →  
BonusComponent 3 3 →  
CompensationPackage 3 3 → BaseSalaryComponent  
StockCompensationComponent 4 3 →  

### core (5 классов, 18 полей, 20 методов)
Employee 8 4 → Position, OrganizationUnit, EmploymentContract, CompensationPackage  
EmploymentContract 4 3 → Employee  
OrganizationUnit 4 4 → Employee  
Payee 3 4 →  
Position 5 3 →  

### deductions (5 классов, 14 полей, 13 методов)
BenefitDeduction 3 3 →  
DeductionRule 3 3 →  
Garnishment 3 3 →  
TaxDeduction 3 3 →  
VoluntaryDeduction 3 2 →  

### hr (5 классов, 17 полей, 13 методов)
BenefitEnrollment 5 3 → BenefitDeduction  
OnboardingChecklist 4 3 →  
PerformanceReview 4 3 →  
RecruitmentRecord 4 3 →  
TerminationRecord 5 3 →  

### integrations (5 классов, 16 полей, 16 методов)
AuditLogger 4 3 →  
ConfigService 3 3 →  
NotificationService 4 3 →  
PayrollFileImporter 4 3 →  
Repository 3 4 →  

### payments (5 классов, 18 полей, 17 методов)
BankTransferAdapter 5 3 → PaymentGatewayAdapter, PaymentInstruction  
CashPaymentProcessor 4 3 →  
PaymentBatch 4 3 → PaymentInstruction  
PaymentGatewayAdapter 3 3 → PaymentInstruction  
PaymentInstruction 3 3 → Payee  

### payroll (5 классов, 26 полей, 20 методов)
PayrollRecord 4 3 → Employee  
PayRun 7 8 → PayrollRecord, PaymentBatch  
Payslip 4 3 → PayrollRecord  
RetroAdjustment 5 3 → PayrollRecord  
SalaryCalculator 6 3 → CompensationPackage, DeductionRule, Employee  

### reporting (5 классов, 20 полей, 16 методов)
ExportService 4 3 →  
GLMapper 4 3 →  
PayrollAnalytics 4 3 →  
ReconciliationEngine 4 3 →  
ReportGenerator 5 3 → GLMapper  

### taxes (5 классов, 17 полей, 14 методов)
EmployerContributions 3 3 →  
TaxAuthority 3 3 →  
TaxConfig 4 3 → TaxAuthority  
TaxFiling 4 3 → TaxAuthority  
WithholdingSchedule 4 4 →  

### time (5 классов, 17 полей, 14 методов)
LeaveRequest 4 3 → Employee  
OvertimePolicy 3 3 →  
Schedule 4 3 →  
TimeEntry 3 3 →  
TimeSheet 5 3 → TimeEntry, OvertimePolicy  

---

## Статистика проекта

- **Классы:** 50  
- **Поля:** 156  
- **Методы:** 102  
- **Ассоциации:** 30  
- **Исключения:** 12  
