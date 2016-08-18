# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0018_customer_receipt_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='associate',
            name='image_url',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
