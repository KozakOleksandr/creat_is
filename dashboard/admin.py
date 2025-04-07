from django.contrib import admin
from .models import SystemSettings


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('detection_confidence', 'iou_threshold', 'use_gpu', 'processing_resolution')
    fieldsets = (
        ('Параметри виявлення', {
            'fields': ('detection_confidence', 'iou_threshold', 'max_detection_count')
        }),
        ('Продуктивність', {
            'fields': ('use_gpu', 'processing_resolution')
        }),
    )

    def has_add_permission(self, request):
        # Забороняємо додавання більше одного запису
        if self.model.objects.exists():
            return False
        return True