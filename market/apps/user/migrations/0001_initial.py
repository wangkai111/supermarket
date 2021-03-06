# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-18 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=32)),
                ('telephone', models.SmallIntegerField(max_length=11)),
                ('sex', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=3)),
                ('isDelete', models.BooleanField(default=False)),
                ('birthday', models.DateField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('school_name', models.CharField(max_length=25)),
                ('address', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
