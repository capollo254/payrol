from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .forms import UserChangeForm, UserCreationForm
from .models import User, CompanySettings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    # Redefine the fieldsets to exclude the 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )

    list_display = ['email', 'is_staff', 'is_superuser']
    ordering = ('email',)
    search_fields = ('email',)


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    """Admin interface for Company Settings"""
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'logo')
        }),
        ('Contact Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'postal_code', 'country', 'phone', 'email', 'website')
        }),
    )
    
    list_display = ('company_name', 'logo_preview', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    def logo_preview(self, obj):
        """Display a small preview of the logo"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.logo.url
            )
        return "No logo uploaded"
    logo_preview.short_description = "Logo Preview"
    
    def has_add_permission(self, request):
        """Only allow one company settings instance"""
        return not CompanySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of company settings"""
        return False