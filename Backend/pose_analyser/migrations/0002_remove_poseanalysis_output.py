# Generated by Django 3.0 on 2022-02-05 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pose_analyser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poseanalysis',
            name='output',
        ),
    ]
