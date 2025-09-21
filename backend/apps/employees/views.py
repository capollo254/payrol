# apps/employees/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Employee, JobInformation, VoluntaryDeduction, EmployeeBenefit
from .serializers import EmployeeSerializer, JobInformationSerializer, VoluntaryDeductionSerializer, EmployeeBenefitSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return employees based on user permissions
        """
        user = self.request.user
        
        # If user is superuser, they can see all employees
        if user.is_superuser:
            return Employee.objects.all().order_by('user__last_name')
        
        # Regular employees can only see their own profile
        try:
            employee = user.employee_profile
            return Employee.objects.filter(id=employee.id)
        except Exception:
            # If user has no employee profile, return empty queryset
            return Employee.objects.none()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Returns the current user's employee profile.
        """
        try:
            employee = Employee.objects.get(user=request.user)
            serializer = self.get_serializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee profile not found for current user'}, status=404)

    @action(detail=True, methods=['get'])
    def gross_salary(self, request, pk=None):
        employee = self.get_object()
        return Response({'gross_salary': employee.gross_salary})
    
class JobInformationViewSet(viewsets.ModelViewSet):
    serializer_class = JobInformationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return job information based on user permissions
        """
        user = self.request.user
        
        # If user is superuser, they can see all job information
        if user.is_superuser:
            return JobInformation.objects.all().order_by('employee__user__last_name')
        
        # Regular employees can only see their own job information
        try:
            employee = user.employee_profile
            return JobInformation.objects.filter(employee=employee)
        except Exception:
            return JobInformation.objects.none()

class VoluntaryDeductionViewSet(viewsets.ModelViewSet):
    serializer_class = VoluntaryDeductionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return voluntary deductions based on user permissions
        """
        user = self.request.user
        
        # If user is superuser, they can see all deductions
        if user.is_superuser:
            return VoluntaryDeduction.objects.all()
        
        # Regular employees can only see their own deductions
        try:
            employee = user.employee_profile
            return VoluntaryDeduction.objects.filter(employee=employee)
        except Exception:
            return VoluntaryDeduction.objects.none()

class EmployeeBenefitViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeBenefitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return employee benefits based on user permissions
        """
        user = self.request.user
        
        # If user is superuser, they can see all benefits
        if user.is_superuser:
            return EmployeeBenefit.objects.all()
        
        # Regular employees can only see their own benefits
        try:
            employee = user.employee_profile
            return EmployeeBenefit.objects.filter(employee=employee)
        except Exception:
            return EmployeeBenefit.objects.none()