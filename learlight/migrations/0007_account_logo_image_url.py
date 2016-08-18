# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0006_auto_20150721_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='logo_image_url',
            field=models.CharField(default='https://s3.amazonaws.com/learlight-assets/email-jewlery-logo.png', max_length=1000),
            preserve_default=False,
        ),
    ]
