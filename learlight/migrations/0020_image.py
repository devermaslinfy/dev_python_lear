# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0019_associate_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField()),
                ('updated_by', models.IntegerField()),
                ('url', models.CharField(max_length=1000)),
                ('category', models.CharField(max_length=16)),
                ('customer', models.ForeignKey(to='learlight.Customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
