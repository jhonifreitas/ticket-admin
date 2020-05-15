from django.contrib import admin

from ticket_admin.payment import models


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'user', 'image', 'date', 'status', 'updated_at', 'created_at']
    list_display_links = ['id', 'user']
