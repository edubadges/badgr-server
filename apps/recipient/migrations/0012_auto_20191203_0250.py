# Generated by Django 2.2.7 on 2019-12-03 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipient', '0011_auto_20171025_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipientgroup',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
