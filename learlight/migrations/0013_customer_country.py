# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0012_auto_20150809_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.CharField(max_length=2, null=True, blank=True),
        ),
    ]
