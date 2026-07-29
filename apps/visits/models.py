from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.patients.models import Patient


class Visit(models.Model):
    """Visit/appointment record."""

    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Насрочен'
        IN_PROGRESS = 'in_progress', 'В процес'
        COMPLETED = 'completed', 'Завършен'
        CANCELLED = 'cancelled', 'Отменен'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits', verbose_name='Пациент')
    veterinarian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='visits',
        verbose_name='Ветеринар'
    )

    date = models.DateTimeField(default=timezone.now, verbose_name='Дата')
    reason = models.CharField(max_length=255, verbose_name='Причина', help_text='Причина за посещението')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED, verbose_name='Статус')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Създаден на')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновен на')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Преглед'
        verbose_name_plural = 'Прегледи'

    def __str__(self):
        return f"{self.patient.name} - {self.date.date()} - {self.reason[:30]}"


class ExamNotes(models.Model):
    """Examination notes for a visit."""

    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name='exam_notes', verbose_name='Преглед')

    symptoms = models.TextField(blank=True, verbose_name='Симптоми', help_text='Наблюдавани симптоми')
    diagnosis = models.TextField(blank=True, verbose_name='Диагноза', help_text='Диагноза')
    treatment_plan = models.TextField(blank=True, verbose_name='План за лечение', help_text='План за лечение')
    follow_up_notes = models.TextField(blank=True, verbose_name='Бележки за контролен преглед', help_text='Инструкции за контролен преглед')

    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Температура', help_text='Температура в градуси по Целзий')
    heart_rate = models.PositiveIntegerField(null=True, blank=True, verbose_name='Сърдечен ритъм', help_text='Сърдечен ритъм (уд/мин)')
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True, verbose_name='Дихателна честота', help_text='Дихателна честота (вдишвания/мин)')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Създаден на')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновен на')

    class Meta:
        verbose_name = 'Бележки от преглед'
        verbose_name_plural = 'Бележки от прегледи'

    def __str__(self):
        return f"Бележки от преглед за {self.visit}"


class Manipulation(models.Model):
    """Procedures/manipulations performed during a visit."""

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='manipulations', verbose_name='Преглед')

    name = models.CharField(max_length=200, verbose_name='Наименование', help_text='Наименование на процедурата')
    description = models.TextField(blank=True, verbose_name='Описание', help_text='Описание на процедурата')
    notes = models.TextField(blank=True, verbose_name='Бележки', help_text='Допълнителни бележки')

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Извършена от'
    )
    performed_at = models.DateTimeField(default=timezone.now, verbose_name='Извършена на')

    class Meta:
        ordering = ['-performed_at']
        verbose_name = 'Манипулация'
        verbose_name_plural = 'Манипулации'

    def __str__(self):
        return f"{self.name} - {self.visit.patient.name}"


class Vaccination(models.Model):
    """Vaccination records."""

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='vaccinations', verbose_name='Преглед')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vaccinations', verbose_name='Пациент')

    vaccine_name = models.CharField(max_length=200, verbose_name='Име на ваксината')
    batch_number = models.CharField(max_length=100, blank=True, verbose_name='Партиден номер')
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='Производител')

    administered_at = models.DateTimeField(default=timezone.now, verbose_name='Приложена на')
    administered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Приложена от'
    )

    next_due_date = models.DateField(null=True, blank=True, verbose_name='Следваща дата', help_text='Следваща дата за ваксинация')
    notes = models.TextField(blank=True, verbose_name='Бележки')

    class Meta:
        ordering = ['-administered_at']
        verbose_name = 'Ваксинация'
        verbose_name_plural = 'Ваксинации'

    def __str__(self):
        return f"{self.vaccine_name} - {self.patient.name} ({self.administered_at.date()})"


class Prescription(models.Model):
    """Prescription records."""

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='prescriptions', verbose_name='Преглед')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions', verbose_name='Пациент')

    medication = models.CharField(max_length=200, verbose_name='Медикамент')
    dosage = models.CharField(max_length=100, verbose_name='Дозировка', help_text='напр. 10мг')
    frequency = models.CharField(max_length=100, verbose_name='Честота', help_text='напр. два пъти дневно')
    duration = models.CharField(max_length=100, verbose_name='Продължителност', help_text='напр. 7 дни')
    instructions = models.TextField(blank=True, verbose_name='Инструкции', help_text='Специални инструкции')

    prescribed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Предписано от'
    )
    prescribed_at = models.DateTimeField(default=timezone.now, verbose_name='Предписано на')

    class Meta:
        ordering = ['-prescribed_at']
        verbose_name = 'Рецепта'
        verbose_name_plural = 'Рецепти'

    def __str__(self):
        return f"{self.medication} - {self.patient.name}"


class LabResult(models.Model):
    """Lab result file uploads."""

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='lab_results', verbose_name='Преглед')

    title = models.CharField(max_length=200, verbose_name='Заглавие')
    description = models.TextField(blank=True, verbose_name='Описание')
    file = models.FileField(upload_to='lab_results/%Y/%m/', verbose_name='Файл')

    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Качен на')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Качен от'
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Лабораторен резултат'
        verbose_name_plural = 'Лабораторни резултати'

    def __str__(self):
        return f"{self.title} - {self.visit.patient.name}"


class Attachment(models.Model):
    """General file attachments (X-rays, documents, etc.)."""

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='attachments', verbose_name='Преглед')

    title = models.CharField(max_length=200, verbose_name='Заглавие')
    description = models.TextField(blank=True, verbose_name='Описание')
    file = models.FileField(upload_to='attachments/%Y/%m/', verbose_name='Файл')

    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Качен на')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Качен от'
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Прикачен файл'
        verbose_name_plural = 'Прикачени файлове'

    def __str__(self):
        return f"{self.title} - {self.visit.patient.name}"


class Deworming(models.Model):
    """Deworming/decontamination records (Обезпаразитяване)."""

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='dewormings', verbose_name='Преглед')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='dewormings', verbose_name='Пациент')

    product_name = models.CharField(max_length=200, verbose_name='Препарат', help_text='Име на препарата')
    dose = models.CharField(max_length=100, blank=True, verbose_name='Доза')
    batch_number = models.CharField(max_length=100, blank=True, verbose_name='Партиден номер')
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='Производител')

    administered_at = models.DateTimeField(default=timezone.now, verbose_name='Приложено на')
    administered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Приложено от'
    )

    next_due_date = models.DateField(null=True, blank=True, verbose_name='Следваща дата', help_text='Следваща дата за обезпаразитяване')
    notes = models.TextField(blank=True, verbose_name='Бележки')

    class Meta:
        ordering = ['-administered_at']
        verbose_name = 'Обезпаразитяване'
        verbose_name_plural = 'Обезпаразитявания'

    def __str__(self):
        return f"{self.product_name} - {self.patient.name} ({self.administered_at.date()})"


class VisitLog(models.Model):
    """Audit log for tracking who did what on a visit."""

    class ActionType(models.TextChoices):
        CREATED = 'created', 'Създаден'
        UPDATED = 'updated', 'Обновен'
        EXAM_NOTES = 'exam_notes', 'Бележки от преглед'
        MANIPULATION = 'manipulation', 'Манипулация'
        VACCINATION = 'vaccination', 'Ваксинация'
        PRESCRIPTION = 'prescription', 'Рецепта'
        DEWORMING = 'deworming', 'Обезпаразитяване'
        LAB_RESULT = 'lab_result', 'Лабораторен резултат'
        ATTACHMENT = 'attachment', 'Прикачен файл'
        STATUS_CHANGE = 'status_change', 'Промяна на статус'

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='logs', verbose_name='Преглед')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Потребител'
    )

    action = models.CharField(max_length=20, choices=ActionType.choices, verbose_name='Действие')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запис от дневник'
        verbose_name_plural = 'Записи от дневник'

    def __str__(self):
        return f"{self.get_action_display()} - {self.visit} ({self.created_at})"
