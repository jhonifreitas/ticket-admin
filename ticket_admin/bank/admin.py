from django.contrib import admin

from ticket_admin.bank import models


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'user', 'name', 'updated_at', 'created_at']
    list_display_links = ['id', 'user']
