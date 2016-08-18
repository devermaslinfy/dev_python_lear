# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0016_customer_county'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='initials',
        ),
        migrations.AddField(
            model_name='customer',
            name='authorized',
            field=models.BooleanField(default=False),
        ),
    ]
