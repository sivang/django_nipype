# Generated by Django 2.1.4 on 2019-02-01 14:44

from django.db import migrations, models
import django.db.models.deletion
import django_nipype.models.fields
import django_nipype.models.interfaces.fsl.bet.bet_run


class Migration(migrations.Migration):

    dependencies = [
        ('django_nipype', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='betresults',
            name='run',
        ),
        migrations.AddField(
            model_name='betrun',
            name='results',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='results_for', to='django_nipype.BetResults'),
        ),
        migrations.AlterField(
            model_name='betrun',
            name='output',
            field=django_nipype.models.fields.ChoiceArrayField(base_field=models.CharField(choices=[('BRN', 'Brain'), ('SRF', 'Surface Outline'), ('MSK', 'Binary Mask'), ('SKL', 'Skull'), ('MSH', 'Mesh Surface')], max_length=3), blank=True, default=django_nipype.models.interfaces.fsl.bet.bet_run.default_output, size=5),
        ),
    ]