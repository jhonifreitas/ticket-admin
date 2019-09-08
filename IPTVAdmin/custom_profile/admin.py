from django.contrib import admin

from IPTVAdmin.custom_profile import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'config', 'name', 'phone', 'updated_at', 'created_at']
    list_display_links = ['id', 'config']
    readonly_fields = ['config', 'name', 'phone', 'cpf', 'email']
