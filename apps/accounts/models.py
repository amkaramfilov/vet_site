from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based access."""

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        VETERINARIAN = 'veterinarian', 'Ветеринар'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VETERINARIAN,
        verbose_name='Роля',
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    specialization = models.CharField(max_length=100, blank=True, verbose_name='Специализация', help_text='напр. Хирургия, Дентална медицина, Вътрешни болести')

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Потребител'
        verbose_name_plural = 'Потребители'

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_veterinarian(self):
        return self.role == self.Role.VETERINARIAN
