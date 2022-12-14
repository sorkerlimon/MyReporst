# Generated by Django 3.2.15 on 2022-10-16 12:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_email'),
        ('medical_report', '0019_imagetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='absoluteleukocytecount',
            name='imageid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical_report.imageadd'),
        ),
        migrations.AddField(
            model_name='totallcount',
            name='imageid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical_report.imageadd'),
        ),
        migrations.CreateModel(
            name='Esrcount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esr', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('imageid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical_report.imageadd')),
            ],
        ),
        migrations.CreateModel(
            name='Differentialleukocytecount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('neutrophil2', models.FloatField(blank=True, null=True)),
                ('lymphocyte2', models.FloatField(blank=True, null=True)),
                ('monocyte2', models.FloatField(blank=True, null=True)),
                ('eosinophil2', models.FloatField(blank=True, null=True)),
                ('basophil2', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('imageid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medical_report.imageadd')),
            ],
        ),
    ]
