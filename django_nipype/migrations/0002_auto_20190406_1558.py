# Generated by Django 2.2 on 2019-04-06 15:58

from django.db import migrations, models
import django.db.models.deletion
import django_nipype.models.interfaces.fsl.bet.choices.mode


class Migration(migrations.Migration):

    dependencies = [
        ('django_nipype', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='betconfiguration',
            name='mode',
            field=models.CharField(choices=[('NORMAL', 'Normal'), ('ROBUST', 'Robust'), ('PADDNG', 'Padding'), ('REMOVE', 'Remove Eyes'), ('SURFAC', 'Surfaces'), ('FUNCTN', 'Funational'), ('REDUBI', 'Reduce Bias')], default=django_nipype.models.interfaces.fsl.bet.choices.mode.Mode('Normal'), max_length=6),
        ),
        migrations.AlterField(
            model_name='betrun',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='run_set', to='django_nipype.BetConfiguration'),
        ),
    ]
