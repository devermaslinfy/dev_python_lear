# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0021_auto_20150918_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='stores',
            field=models.ManyToManyField(related_name='store_account', to='learlight.Account', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='transaction_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='category',
            field=models.CharField(max_length=16, choices=[(b'receipt', b'Receipt'), (b'jewelry', b'Jewelry')]),
        ),
    ]
