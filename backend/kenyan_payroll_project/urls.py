# kenyan_payroll_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import welcome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', welcome, name='welcome'),
    path('api/v1/auth/', include('apps.core.urls')),
    path('api/v1/employees/', include('apps.employees.urls')),
    path('api/v1/payroll/', include('apps.payroll.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/leaves/', include('apps.leaves.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)