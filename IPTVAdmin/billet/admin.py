from django.contrib import admin

from IPTVAdmin.billet import models


@admin.register(models.Billet)
class BilletAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'profile', 'updated_at', 'created_at']
    list_display_links = ['id', 'profile']
