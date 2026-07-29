from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date

from apps.clients.models import Client


class Patient(models.Model):
    """Pet/Patient model with detailed information."""

    class Gender(models.TextChoices):
        MALE = 'male', 'Мъжки'
        FEMALE = 'female', 'Женски'
        UNKNOWN = 'unknown', 'Неизвестен'

    # Basic Info
    name = models.CharField(max_length=100, verbose_name='Име')
    species = models.CharField(max_length=100, verbose_name='Вид', help_text='напр. Куче, Котка, Птица')
    breed = models.CharField(max_length=100, blank=True, verbose_name='Порода')
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.UNKNOWN, verbose_name='Пол')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата на раждане')
    color = models.CharField(max_length=100, blank=True, verbose_name='Цвят', help_text='Цвят на козината или отличителни белези')
    microchip_number = models.CharField(max_length=50, blank=True, unique=True, null=True, verbose_name='Номер на микрочип')
    photo = models.ImageField(upload_to='patients/photos/', blank=True, null=True, verbose_name='Снимка')

    # Medical Info
    allergies = models.TextField(blank=True, verbose_name='Алергии', help_text='Известни алергии')
    chronic_conditions = models.TextField(blank=True, verbose_name='Хронични заболявания', help_text='Хронични заболявания или продължаващи здравословни проблеми')
    notes = models.TextField(blank=True, verbose_name='Бележки', help_text='Общи бележки за пациента')

    # Relationships
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='patients', verbose_name='Собственик')

    # Audit
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Създаден на')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновен на')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_patients',
        verbose_name='Създаден от'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенти'

    def __str__(self):
        return f"{self.name} ({self.species})"

    @property
    def age(self):
        """Calculate age from date of birth."""
        if not self.date_of_birth:
            return None
        today = date.today()
        years = today.year - self.date_of_birth.year
        months = today.month - self.date_of_birth.month
        if months < 0:
            years -= 1
            months += 12
        if years > 0:
            return f"{years} год{'ини' if years != 1 else 'ина'}"
        elif months > 0:
            return f"{months} месец{'а' if months != 1 else ''}"
        else:
            days = (today - self.date_of_birth).days
            return f"{days} {'дни' if days != 1 else 'ден'}"

    @property
    def current_weight(self):
        """Get the most recent weight record."""
        latest = self.weight_history.first()
        return latest.weight if latest else None

    def save(self, *args, **kwargs):
        # Ensure microchip_number is None if empty (for unique constraint)
        if not self.microchip_number:
            self.microchip_number = None
        super().save(*args, **kwargs)


class WeightRecord(models.Model):
    """Weight history tracking for patients."""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='weight_history', verbose_name='Пациент')
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Тегло', help_text='Тегло в кг')
    recorded_at = models.DateTimeField(default=timezone.now, verbose_name='Записано на')
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Записано от'
    )
    notes = models.CharField(max_length=255, blank=True, verbose_name='Бележки')

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Запис за тегло'
        verbose_name_plural = 'Записи за тегло'

    def __str__(self):
        return f"{self.patient.name} - {self.weight}кг на {self.recorded_at.date()}"
