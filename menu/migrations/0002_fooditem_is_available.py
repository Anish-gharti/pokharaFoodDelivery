# Generated by Django 4.1.7 on 2023-04-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
