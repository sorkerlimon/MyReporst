# Generated by Django 3.2.16 on 2022-10-13 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_report', '0006_auto_20221007_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageadd',
            name='date',
            field=models.DateField(),
        ),
    ]
