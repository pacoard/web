# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-31 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import economy.models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0006_emailsubscriber_newsletter'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaderboardRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(db_index=True, default=economy.models.get_time)),
                ('modified_on', models.DateTimeField(default=economy.models.get_time)),
                ('github_username', models.CharField(max_length=255)),
                ('leaderboard', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('active', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
