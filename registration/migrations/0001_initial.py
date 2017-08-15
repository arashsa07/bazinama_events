# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-12 10:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import registration.models
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer starting with a letter. Letters, digits and underscore only.', max_length=32, unique=True, validators=[utils.validators.UsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('phone_number', models.BigIntegerField(blank=True, error_messages={'unique': 'A user with this mobile number already exists.'}, null=True, unique=True, validators=[utils.validators.PhoneNumberValidator()], verbose_name='mobile number')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('verify_codes', models.CommaSeparatedIntegerField(blank=True, max_length=30, verbose_name='verification codes')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'db_table': 'auth_users',
            },
            managers=[
                ('objects', registration.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=150, verbose_name='city name')),
            ],
            options={
                'ordering': ('city_name',),
                'verbose_name_plural': 'cities',
                'verbose_name': 'city',
                'db_table': 'locations_cities',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=100, verbose_name='state name')),
            ],
            options={
                'ordering': ('state_name',),
                'verbose_name_plural': 'states',
                'verbose_name': 'state',
                'db_table': 'locations_states',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(blank=True, max_length=150, verbose_name='nick_name')),
                ('avatar', models.ImageField(blank=True, upload_to='', verbose_name='avatar')),
                ('birthday', models.DateField(verbose_name='birthday')),
                ('gender', models.NullBooleanField(help_text='female is False, male is True, null is unset', verbose_name='gender')),
                ('cup_numbers', models.PositiveIntegerField(verbose_name='Cup Numbers')),
                ('level', models.PositiveSmallIntegerField(verbose_name='Level')),
                ('clash_id', models.CharField(max_length=256, verbose_name='Clash ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='registration.City')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'profiles',
                'verbose_name': 'profile',
                'db_table': 'auth_profiles',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.State', verbose_name='state'),
        ),
    ]