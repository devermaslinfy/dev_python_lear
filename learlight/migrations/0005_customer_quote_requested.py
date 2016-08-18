# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0004_auto_20150710_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='quote_requested',
            field=models.BooleanField(default=False),
        ),
    ]
