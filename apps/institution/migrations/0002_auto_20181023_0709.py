# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-23 14:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name_plural': 'faculties'},
        ),
    ]
