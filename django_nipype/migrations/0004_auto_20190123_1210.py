# Generated by Django 2.1.5 on 2019-01-23 12:10

from django.db import migrations, models
import django_nipype.models.fields
import django_nipype.models.interfaces.fsl.bet.bet_configuration


class Migration(migrations.Migration):

    dependencies = [
        ('django_nipype', '0003_auto_20190122_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='betconfiguration',
            name='no_output',
        ),
        migrations.RemoveField(
            model_name='betconfiguration',
            name='output_binary_mask',
        ),
        migrations.RemoveField(
            model_name='betconfiguration',
            name='output_mesh_surface',
        ),
        migrations.RemoveField(
            model_name='betconfiguration',
            name='output_skull',
        ),
        migrations.RemoveField(
            model_name='betconfiguration',
            name='output_surface_outline',
        ),
        migrations.AddField(
            model_name='betconfiguration',
            name='output',
            field=django_nipype.models.fields.ChoiceArrayField(base_field=models.CharField(choices=[('BRN', 'Brain'), ('SRF', 'Surface Outline'), ('MSK', 'Binary Mask'), ('SURF', 'Surfaces'), ('FUNC', 'Functional')], max_length=3), blank=True, default=django_nipype.models.interfaces.fsl.bet.bet_configuration.default_output, size=5),
        ),
    ]
