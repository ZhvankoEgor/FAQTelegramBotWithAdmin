# Generated by Django 3.2.7 on 2021-12-14 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ', '0007_settings_bot'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings_bot',
            options={'verbose_name': 'Настройки бота', 'verbose_name_plural': 'Настройки бота'},
        ),
    ]