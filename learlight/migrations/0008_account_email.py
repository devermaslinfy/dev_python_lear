# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0007_account_logo_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email',
            field=models.EmailField(default='learlabscrm@mg.learlabscrm.com', max_length=254),
            preserve_default=False,
        ),
    ]
