from django.contrib import admin
from .models import Visit, ExamNotes, Manipulation, Vaccination, Prescription, LabResult, Attachment


class ExamNotesInline(admin.StackedInline):
    model = ExamNotes
    extra = 0


class ManipulationInline(admin.TabularInline):
    model = Manipulation
    extra = 0


class VaccinationInline(admin.TabularInline):
    model = Vaccination
    extra = 0


class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0


class LabResultInline(admin.TabularInline):
    model = LabResult
    extra = 0


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date', 'reason', 'veterinarian', 'status', 'created_at']
    list_filter = ['status', 'date', 'veterinarian']
    search_fields = ['patient__name', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ExamNotesInline, ManipulationInline, VaccinationInline, PrescriptionInline, LabResultInline, AttachmentInline]


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ['vaccine_name', 'patient', 'administered_at', 'next_due_date']
    list_filter = ['administered_at', 'next_due_date']
    search_fields = ['vaccine_name', 'patient__name']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication', 'patient', 'dosage', 'frequency', 'prescribed_at']
    list_filter = ['prescribed_at']
    search_fields = ['medication', 'patient__name']
