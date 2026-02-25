"""
Admin configuration for screening app.
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import ScreeningResult, SanctionsList


@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):
    """Admin for screening results."""

    list_display = (
        'merchant',
        'screening_type',
        'screened_entity',
        'status_display',
        'matched_list',
        'screened_at',
    )

    list_filter = ('status', 'screening_type', 'screened_at')
    search_fields = ('merchant__business_name', 'screened_entity', 'matched_list')
    readonly_fields = ('screened_at',)

    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            'CLEAR': 'green',
            'MATCH': 'red',
            'POTENTIAL_MATCH': 'orange',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'


@admin.register(SanctionsList)
class SanctionsListAdmin(admin.ModelAdmin):
    """Admin for sanctions lists reference."""

    list_display = ('name', 'source', 'last_updated', 'is_active')
    list_filter = ('is_active', 'source')
    search_fields = ('name', 'source')
