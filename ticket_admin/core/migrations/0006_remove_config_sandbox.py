# Generated by Django 2.2.10 on 2020-05-13 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_config_sandbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='sandbox',
        ),
    ]
