# Generated by Django 4.2.5 on 2023-10-09 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_arq', '0006_mensaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
    ]
