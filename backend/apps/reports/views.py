# apps/reports/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ReportGenerationLog
from .serializers import ReportGenerationLogSerializer
from apps.employees.models import Employee
from django.utils import timezone
import os

class ReportViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for generating and managing reports.
    """
    queryset = ReportGenerationLog.objects.all().order_by('-generation_date')
    serializer_class = ReportGenerationLogSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        # The user generating the report is the currently authenticated user
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee profile not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # For this example, we'll simulate a file path.
        # In a real app, this would be a more complex generation process.
        report_type = self.request.data.get('report_type')
        start_date = self.request.data.get('start_date')
        end_date = self.request.data.get('end_date')

        file_path = f"reports/{report_type}_{timezone.now().strftime('%Y%m%d%H%M%S')}.pdf"

        serializer.save(
            generated_by=employee,
            file_path=file_path,
            start_date=start_date,
            end_date=end_date
        )

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Action to download a generated report.
        """
        report_log = self.get_object()
        # This is a placeholder. A real implementation would serve the file.
        file_exists = os.path.exists(report_log.file_path)

        if not file_exists:
            return Response(
                {"error": "Report file not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # In a real application, you would return a FileResponse or similar
        return Response(
            {"message": f"Simulating download of {report_log.file_path}"},
            status=status.HTTP_200_OK
        )