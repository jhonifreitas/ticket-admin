from django.contrib import admin

from ticket_admin.custom_profile import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'user', 'name', 'phone', 'updated_at', 'created_at']
    list_display_links = ['id', 'user']


@admin.register(models.ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'profile', 'username', 'password', 'status', 'updated_at', 'created_at']
    list_display_links = ['id', 'profile']
