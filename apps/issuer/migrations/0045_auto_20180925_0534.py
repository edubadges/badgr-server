# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-25 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0044_auto_20180713_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgeinstance',
            name='recipient_identifier',
            field=models.CharField(db_index=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='badgeinstance',
            name='recipient_type',
            field=models.CharField(choices=[('email', 'email'), ('openBadgeId', 'openBadgeId'), ('telephone', 'telephone'), ('url', 'url'), ('eduID', 'eduID')], default='email', max_length=255),
        ),
    ]