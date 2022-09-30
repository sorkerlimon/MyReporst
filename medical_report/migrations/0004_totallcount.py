# Generated by Django 3.2.15 on 2022-09-30 16:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_email'),
        ('medical_report', '0003_imageadd'),
    ]

    operations = [
        migrations.CreateModel(
            name='Totallcount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hbg', models.FloatField(blank=True, null=True)),
                ('rbc', models.FloatField(blank=True, null=True)),
                ('wbc', models.FloatField(blank=True, null=True)),
                ('plt', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]