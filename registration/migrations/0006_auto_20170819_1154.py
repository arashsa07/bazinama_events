# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-19 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20170816_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cup_numbers',
            field=models.PositiveIntegerField(verbose_name='cup'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nick_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='name'),
        ),
    ]
