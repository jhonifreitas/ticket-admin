from django.contrib import admin

from ticket_admin.panel import models


@admin.register(models.Panel)
class PanelAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'user', 'name', 'updated_at', 'created_at']
    list_display_links = ['id', 'user']
