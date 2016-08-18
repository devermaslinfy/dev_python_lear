# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0013_customer_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='account',
            field=models.ForeignKey(default=1, to='learlight.Account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='associate',
            field=models.ForeignKey(default=4, to='learlight.Associate'),
            preserve_default=False,
        ),
    ]
