# Generated by Django 5.1.2 on 2025-01-24 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='images',
            field=models.TextField(default='', verbose_name='Изображения'),
        ),
    ]
