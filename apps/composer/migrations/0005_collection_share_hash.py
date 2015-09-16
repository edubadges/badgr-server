# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('composer', '0004_auto_20150605_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='share_hash',
            field=models.CharField(default='', max_length=255, blank=True),
            preserve_default=False,
        ),
    ]
