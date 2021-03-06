# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 10:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_remove_userprofile_registration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 6, 20, 10, 54, 4, 659105, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/img.jpg'),
        ),
    ]
