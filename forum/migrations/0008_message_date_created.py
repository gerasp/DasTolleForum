# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 13:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20160620_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 6, 20, 13, 2, 38, 659626, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
