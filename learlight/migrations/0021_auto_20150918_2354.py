# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0020_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='jewelry_image_url',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='receipt_image_url',
        ),
    ]
