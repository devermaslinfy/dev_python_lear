# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0003_auto_20150708_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='initials',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
