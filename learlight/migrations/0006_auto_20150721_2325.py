# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0005_customer_quote_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.CharField(default='92 Jackson St.', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='phone_number',
            field=models.CharField(default='978-745-2517', max_length=15),
            preserve_default=False,
        ),
    ]
