from django.contrib import admin

from ticket_admin.billet import models


@admin.register(models.Billet)
class BilletAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'dueDate', 'get_user', 'profile', 'status', 'created_at']
    list_display_links = ['id', 'dueDate']
    readonly_fields = ['profile', 'code', 'paymentLink', 'reference', 'numberOfPayments', 'instructions',
                       'description', 'amount']

    def get_user(self, obj):
        return obj.profile.user
    get_user.short_description = 'Usuário'
