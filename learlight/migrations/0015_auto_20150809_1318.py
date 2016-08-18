# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0014_auto_20150809_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='associate',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
