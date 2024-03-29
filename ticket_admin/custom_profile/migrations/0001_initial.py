# Generated by Django 2.2.1 on 2019-08-08 01:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Deleted at')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('phone', models.CharField(max_length=11, verbose_name='Telefone')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='core.Config', verbose_name='Configuração')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfils',
                'ordering': ['name', '-created_at'],
                'permissions': [('list_profile', 'Pode Listar Perfils')],
            },
        ),
    ]
