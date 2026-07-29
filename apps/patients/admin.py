from django.contrib import admin
from .models import Patient, WeightRecord


class WeightRecordInline(admin.TabularInline):
    model = WeightRecord
    extra = 0
    readonly_fields = ['recorded_at', 'recorded_by']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'breed', 'owner', 'age', 'current_weight', 'created_at']
    list_filter = ['species', 'gender', 'created_at']
    search_fields = ['name', 'microchip_number', 'owner__name']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    inlines = [WeightRecordInline]


@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'weight', 'recorded_at', 'recorded_by']
    list_filter = ['recorded_at']
    search_fields = ['patient__name']
    readonly_fields = ['recorded_at']
