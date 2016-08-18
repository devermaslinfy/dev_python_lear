# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learlight', '0002_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='JewelryType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField()),
                ('updated_by', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='jewelry_image_url',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='jewelry_value',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='initials',
            field=models.CharField(max_length=6),
        ),
        migrations.AddField(
            model_name='customer',
            name='jewelry_type',
            field=models.ForeignKey(blank=True, to='learlight.JewelryType', null=True),
        ),
    ]
