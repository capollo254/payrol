# apps/employees/serializers.py

from rest_framework import serializers
from .models import Employee, VoluntaryDeduction, JobInformation, EmployeeBenefit


class JobInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInformation
        fields = ['company_employee_id', 'kra_pin', 'nssf_number', 'nhif_number', 
                 'department', 'position', 'date_of_joining', 'is_active']


class VoluntaryDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoluntaryDeduction
        fields = ['id', 'name', 'deduction_type', 'calculation_type', 'amount', 
                 'description', 'start_date', 'end_date', 'is_active', 'employee']
        read_only_fields = ['created_at', 'updated_at']


class EmployeeBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBenefit
        fields = ['id', 'name', 'benefit_type', 'calculation_type', 'amount', 
                 'description', 'is_taxable', 'is_active', 'employee']
        read_only_fields = ['created_at', 'updated_at']


class EmployeeSerializer(serializers.ModelSerializer):
    job_information = JobInformationSerializer(source='job_info', read_only=True)
    voluntary_deductions = VoluntaryDeductionSerializer(many=True, read_only=True)
    benefits = EmployeeBenefitSerializer(many=True, read_only=True)
    
    # Use SerializerMethodField to get the full name from the method
    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    def get_full_name(self, obj):
        return obj.full_name()

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'full_name', 'email', 'first_name', 'last_name',
            'gross_salary', 'bank_account_number', 'helb_monthly_deduction', 'is_active',
            'job_information', 'voluntary_deductions', 'benefits'
        ]
        read_only_fields = ['user', 'is_active']