# Generated by Django 2.2.10 on 2020-05-13 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_profile', '0003_auto_20200513_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pay_method',
            field=models.CharField(choices=[('billet', 'Boleto'), ('active', 'Dinheiro'), ('credit_card', 'Cartão de Crédito'), ('transfer', 'Transferência bancária')], default='billet', max_length=255, verbose_name='Forma de Pagamento'),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='status',
            field=models.CharField(choices=[('active', 'Ativo'), ('waiting_payment', 'Aguardando pagamento'), ('expired', 'Vencido'), ('in_test', 'Em teste')], default='active', max_length=255, verbose_name='Status'),
        ),
    ]
