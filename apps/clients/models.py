from django.db import models
from django.conf import settings


class Client(models.Model):
    """Pet owner model."""

    name = models.CharField(max_length=200, verbose_name='Име', help_text='Пълно име на собственика')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    phone_secondary = models.CharField(max_length=20, blank=True, verbose_name='Допълнителен телефон', help_text='Алтернативен телефонен номер')
    email = models.EmailField(blank=True, verbose_name='Имейл')
    address = models.TextField(blank=True, verbose_name='Адрес')
    notes = models.TextField(blank=True, verbose_name='Бележки', help_text='Допълнителни бележки за клиента')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Създаден на')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновен на')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_clients',
        verbose_name='Създаден от'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенти'

    def __str__(self):
        return self.name

    @property
    def pet_count(self):
        return self.patients.count()
