# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0015_auto_20150809_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='county',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
