# Generated by Django 2.1.4 on 2019-02-01 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_nipype', '0002_auto_20190201_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='betresults',
            old_name='brain',
            new_name='out_file',
        ),
    ]