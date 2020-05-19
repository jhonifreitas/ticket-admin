from django.contrib import admin

from ticket_admin.core import models


class TutorialInline(admin.TabularInline):

    model = models.TutorialImage
    exclude = ['deleted_at']
    extra = 1


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'user', 'updated_at', 'created_at']
    list_display_links = ['id', 'user']
    readonly_fields = ['user', 'token', 'instructions_billet', 'description_billet']


@admin.register(models.Tutorial)
class TutorialAdmin(admin.ModelAdmin):

    exclude = ['deleted_at']
    list_display = ['id', 'name', 'updated_at', 'created_at']
    list_display_links = ['id', 'name']
    inlines = [TutorialInline]
