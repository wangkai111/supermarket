# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-24 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_user_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.ImageField(default='head/memtx.png', upload_to='head/%Y%m/%d', verbose_name='用户头像'),
        ),
    ]