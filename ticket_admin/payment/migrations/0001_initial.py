# Generated by Django 2.2.10 on 2020-05-15 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ticket_admin.payment.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('image', models.ImageField(upload_to=ticket_admin.payment.models.get_file_path, verbose_name='Imagem')),
                ('date', models.DateField(verbose_name='Data')),
                ('status', models.CharField(choices=[('approved', 'Aprovado'), ('in_analyze', 'Em análise'), ('not_approved', 'Não aprovado')], default='in_analyze', max_length=255, verbose_name='Status')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Mensagem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
                'ordering': ['-created_at'],
                'permissions': [('list_payment', 'Pode Listar Pagamentos')],
            },
        ),
    ]
