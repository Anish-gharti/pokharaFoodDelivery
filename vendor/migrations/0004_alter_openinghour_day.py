# Generated by Django 3.2.18 on 2023-04-10 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_alter_openinghour_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openinghour',
            name='day',
            field=models.IntegerField(choices=[(1, 'MONDAY'), (2, 'TUESDAY'), (3, 'WEDNESDAY'), (4, 'THRUSDAY'), (5, 'FRIDAY'), (6, 'SATURDAY'), (7, 'SUNDAY')]),
        ),
    ]
