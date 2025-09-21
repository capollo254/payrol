# apps/reports/serializers.py

from rest_framework import serializers
from .models import ReportGenerationLog

class ReportGenerationLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the ReportGenerationLog model.
    """
    generated_by_name = serializers.CharField(source='generated_by.full_name', read_only=True)
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)

    class Meta:
        model = ReportGenerationLog
        fields = [
            'id', 'report_type', 'report_type_display', 'generated_by',
            'generated_by_name', 'generation_date', 'start_date', 'end_date', 'file_path'
        ]
        read_only_fields = ['generated_by', 'generation_date']