# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_message_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(null=True, upload_to='profiles'),
        ),
    ]
