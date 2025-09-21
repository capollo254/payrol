# apps/reports/models.py

from django.db import models
from django.utils import timezone
from apps.employees.models import Employee

class ReportGenerationLog(models.Model):
    """
    A log of generated reports, to be used for an audit trail and download history.
    """
    REPORT_TYPES = (
        ('payslip', 'Payslip Report'),
        ('nssf', 'NSSF Report'),
        ('nhif', 'NHIF Report'),
        ('paye', 'PAYE Report'),
        ('general', 'General Report'),
    )

    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='generated_reports')
    generation_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_report_type_display()} generated on {self.generation_date.strftime('%Y-%m-%d')}"