# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='records',
            name='status',
        ),
        migrations.AddField(
            model_name='records',
            name='corp_status',
            field=models.CharField(choices=[('WI', 'Win'), ('TW', 'Timed Win'), ('TL', 'Timed Loss'), ('LO', 'Lose'), ('TI', 'Tie')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='records',
            name='runner_status',
            field=models.CharField(choices=[('WI', 'Win'), ('TW', 'Timed Win'), ('TL', 'Timed Loss'), ('LO', 'Lose'), ('TI', 'Tie')], max_length=2, null=True),
        ),
    ]