# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-29 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20190129_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='summary',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=64),
        ),
    ]
