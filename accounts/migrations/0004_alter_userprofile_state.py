# Generated by Django 4.1.7 on 2023-04-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
    ]
