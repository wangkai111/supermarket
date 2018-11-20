# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20181119_1321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户管理', 'verbose_name_plural': '用户管理'},
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='位置'),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='生日'),
        ),
        migrations.AddField(
            model_name='user',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='用户名'),
        ),
        migrations.AddField(
            model_name='user',
            name='school_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='学校名字'),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=32, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=11, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]