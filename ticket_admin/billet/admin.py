from django.contrib import admin

from ticket_admin.billet import models


@admin.register(models.Billet)
class BilletAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'profile', 'dueDate', 'status', 'created_at']
    list_display_links = ['id', 'profile']
    readonly_fields = ['profile', 'code', 'paymentLink', 'reference', 'numberOfPayments', 'instructions',
                       'description', 'amount']
