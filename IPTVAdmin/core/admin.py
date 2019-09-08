from django.contrib import admin

from IPTVAdmin.core import models


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'user', 'updated_at', 'created_at']
    list_display_links = ['id', 'user']
    readonly_fields = ['user', 'token', 'instructions_billet', 'description_billet', 'amount_billet']
