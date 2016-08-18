# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0017_auto_20150813_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='receipt_image_url',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
