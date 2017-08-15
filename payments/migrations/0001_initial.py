# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(verbose_name='Creation On', auto_now_add=True)),
                ('updated_time', models.DateTimeField(verbose_name='Modified On', auto_now=True)),
                ('title', models.CharField(verbose_name='gateway title', max_length=100)),
                ('merchant_id', models.CharField(verbose_name='merchant id', blank=True, null=True, max_length=50)),
                ('merchant_pass', models.CharField(verbose_name='merchant pass', blank=True, null=True, max_length=50)),
                ('url', models.CharField(verbose_name='request url', blank=True, null=True, max_length=150)),
                ('check_url', models.CharField(verbose_name='pay check url', blank=True, null=True, max_length=150)),
                ('gw_code', models.PositiveSmallIntegerField(verbose_name='gateway code', choices=[(1, 'Saman'), (2, 'Shaparak'), (3, 'Raad'), (4, 'Bazaar'), (5, 'vas')])),
                ('gw_type', models.PositiveSmallIntegerField(verbose_name='gateway type', choices=[(1, 'BANK'), (2, 'PSP')])),
                ('is_enable', models.BooleanField(verbose_name='is enable', default=True)),
            ],
            options={
                'verbose_name_plural': 'gateways',
                'verbose_name': 'gateway',
                'db_table': 'payments_gateways',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(verbose_name='Creation On', db_index=True, auto_now_add=True)),
                ('updated_time', models.DateTimeField(verbose_name='Modified On', auto_now=True)),
                ('invoice_number', models.UUIDField(verbose_name='invoice number', unique=True, default=uuid.uuid4)),
                ('amount', models.PositiveIntegerField(verbose_name='payment amount', editable=False)),
                ('reference_id', models.CharField(verbose_name='reference id', blank=True, db_index=True, max_length=100)),
                ('user_reference', models.CharField(verbose_name='customer reference', blank=True, max_length=100)),
                ('result_code', models.CharField(verbose_name='result code', blank=True, max_length=100)),
                ('paid_status', models.NullBooleanField(verbose_name='is paid status', editable=False, default=False)),
                ('log', models.TextField(verbose_name='payment log', blank=True)),
                ('vas_token', models.CharField(verbose_name='vas token for vas payments', blank=True, null=True, max_length=100)),
                ('response_type', models.PositiveIntegerField(verbose_name='response type', choices=[(1, 'mobile'), (2, 'web')], default=1)),
                ('gateway', models.ForeignKey(verbose_name='payment gateway', blank=True, related_name='payments', null=True, to='payments.Gateway')),
                ('user', models.ForeignKey(verbose_name='User', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'payments',
                'verbose_name': 'payment',
                'db_table': 'payments',
            },
        ),
    ]
