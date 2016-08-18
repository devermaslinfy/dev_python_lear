# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
from django.conf import settings
import learlight.utils
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learlight', '0008_account_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Associate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField()),
                ('updated_by', models.IntegerField()),
                ('associate_id', models.CharField(default=learlight.utils.generate_id, unique=True, max_length=6)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='account',
            name='external_id',
            field=models.IntegerField(default=learlight.utils.generate_external_id),
        ),
        migrations.AddField(
            model_name='account',
            name='internal_id',
            field=models.CharField(default=learlight.utils.generate_internal_id, max_length=10),
        ),
        migrations.AddField(
            model_name='customer',
            name='purchase_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(related_name='owned_accounts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='postal_code',
            field=localflavor.us.models.USZipCodeField(max_length=10, null=True, blank=True),
        ),
    ]
