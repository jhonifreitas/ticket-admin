from django.contrib import admin

from ticket_admin.custom_profile import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    exclude = ['deleted_at', 'phone', 'cpf', 'email']
    list_display = ['id', 'user', 'name', 'get_phone', 'updated_at', 'created_at']
    list_display_links = ['id', 'user']
    readonly_fields = ['user', 'get_phone', 'get_cpf', 'get_email']

    def get_phone(self, obj):
        part_one = obj.phone[:3]
        part_two = '*'*len(obj.phone[3:])
        return '{}{}'.format(part_one, part_two)
    get_phone.short_description = 'Telefone'

    def get_email(self, obj):
        if obj.email:
            part_one = obj.email[:3]
            part_two = '*'*len(obj.email[3:])
            return '{}{}'.format(part_one, part_two)
        return '---'
    get_email.short_description = 'Email'

    def get_cpf(self, obj):
        if obj.cpf:
            part_one = obj.cpf[:3]
            part_two = '*'*len(obj.cpf[3:])
            return '{}{}'.format(part_one, part_two)
        return '---'
    get_cpf.short_description = 'CPF'


@admin.register(models.ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):

    exclude = ['deleted_at', 'password']
    list_display = ['id', 'profile', 'username', 'get_password', 'status', 'updated_at', 'created_at']
    list_display_links = ['id', 'profile']
    readonly_fields = ['get_password', 'profile']

    def get_password(self, obj):
        part_one = obj.password[:3]
        part_two = '*'*len(obj.password[3:])
        return '{}{}'.format(part_one, part_two)
    get_password.short_description = 'Senha'
