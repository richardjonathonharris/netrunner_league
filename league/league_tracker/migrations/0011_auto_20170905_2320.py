# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 23:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league_tracker', '0010_records_deck'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='league_tracker.Decks')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='league_tracker.Event')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='league_tracker.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='records',
            name='deck',
        ),
        migrations.AddField(
            model_name='records',
            name='deck',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='league_tracker.UserEvent'),
        ),
    ]
