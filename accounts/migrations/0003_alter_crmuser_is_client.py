# Generated by Django 4.1.5 on 2023-02-09 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_crmuser_is_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crmuser',
            name='is_client',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
