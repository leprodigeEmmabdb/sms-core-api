# Generated by Django 5.2.1 on 2025-06-16 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appbroadcastsms', '0003_alter_smpp_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='smpp',
            table='tb_smpp',
        ),
    ]
