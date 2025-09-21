# apps/employees/models.py

from django.db import models
from django.conf import settings
from decimal import Decimal

class Employee(models.Model):
    """
    Core employee profile containing general and payroll-specific information.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    helb_monthly_deduction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # New Relief Fields as per KRA PAYE document
    monthly_insurance_premiums = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Monthly insurance premiums paid (life, health, education policies)"
    )
    monthly_medical_fund_contribution = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Monthly contribution to post-retirement medical fund"
    )
    monthly_mortgage_interest = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Monthly mortgage interest paid for residential property"
    )
    
    is_active = models.BooleanField(default=True)
    
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return self.full_name()

class JobInformation(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='job_info')
    company_employee_id = models.CharField(max_length=50, unique=True, help_text="Company-assigned employee ID")
    kra_pin = models.CharField(max_length=20, unique=True, help_text="Kenya Revenue Authority PIN")
    nssf_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nhif_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.employee.full_name()} - {self.position}"

class VoluntaryDeduction(models.Model):
    """
    Represents an optional deduction from an employee's salary.
    """
    DEDUCTION_TYPES = (
        ('pension', 'Pension Contribution'),
        ('sacco', 'Sacco Contribution'),
        ('loan', 'Check-off Loan'),
        ('insurance', 'Insurance Premium'),
        ('savings', 'Employee Savings'),
        ('other', 'Other'),
    )
    
    CALCULATION_TYPES = (
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage of Salary'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='voluntary_deductions')
    name = models.CharField(max_length=100, help_text="Name of the deduction", default="Unnamed Deduction")
    deduction_type = models.CharField(max_length=50, choices=DEDUCTION_TYPES)
    calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPES, default='fixed')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount or percentage rate", default=0.00)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.full_name()}'s {self.name}"

class EmployeeBenefit(models.Model):
    """
    Represents employee benefits such as allowances and additional compensations.
    """
    BENEFIT_TYPES = (
        ('transport', 'Transport Allowance'),
        ('housing', 'Housing Allowance'),
        ('meal', 'Meal Allowance'),
        ('medical', 'Medical Insurance'),
        ('phone', 'Phone Allowance'),
        ('education', 'Education Allowance'),
        ('other', 'Other'),
    )
    
    CALCULATION_TYPES = (
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage of Salary'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='benefits')
    name = models.CharField(max_length=100, help_text="Name of the benefit")
    benefit_type = models.CharField(max_length=50, choices=BENEFIT_TYPES)
    calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPES, default='fixed')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount or percentage rate")
    description = models.TextField(blank=True, null=True)
    is_taxable = models.BooleanField(default=True, help_text="Whether this benefit is subject to income tax")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.full_name()}'s {self.name}"