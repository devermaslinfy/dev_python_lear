# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import learlight.utils


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0009_auto_20150808_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='internal_id',
            field=models.CharField(default=learlight.utils.generate_internal_id, unique=True, max_length=10),
        ),
    ]
