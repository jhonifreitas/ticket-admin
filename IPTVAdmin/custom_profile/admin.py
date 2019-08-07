from django.contrib import admin

from IPTVAdmin.custom_profile import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'config', 'updated_at', 'created_at']
    list_display_links = ['id', 'config']
