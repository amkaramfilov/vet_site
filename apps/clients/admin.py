from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'pet_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
