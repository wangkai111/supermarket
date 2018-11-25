# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-23 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='active',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('active_name', models.CharField(max_length=50, verbose_name='活动名称')),
                ('image_address', models.ImageField(upload_to='shop_active', verbose_name='图片地址')),
                ('url_address', models.URLField(null=True, verbose_name='活动地址')),
            ],
            options={
                'verbose_name': '首页活动表',
                'verbose_name_plural': '首页活动表',
            },
        ),
        migrations.CreateModel(
            name='active_SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
            ],
            options={
                'verbose_name': '首页专区活动商品表',
                'verbose_name_plural': '首页专区活动商品表',
            },
        ),
        migrations.CreateModel(
            name='active_zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('zone_name', models.CharField(max_length=50, verbose_name='活动专区名称')),
                ('zone_content', models.CharField(blank=True, max_length=255, null=True, verbose_name='活动专区描述')),
                ('zone_order', models.IntegerField(default=0, verbose_name='活动专区排序')),
                ('is_shelf', models.BooleanField(choices=[(1, '上架'), (0, '未上架')], default=0, verbose_name='活动专区是否上架')),
            ],
            options={
                'verbose_name': '首页活动专区',
                'verbose_name_plural': '首页活动专区',
            },
        ),
        migrations.CreateModel(
            name='lunbo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('lunbo_name', models.CharField(max_length=50, verbose_name='轮播名称')),
                ('image_address', models.ImageField(upload_to='shop_lunbo/%Y%m%d', verbose_name='图片地址')),
                ('order', models.IntegerField(default=0, verbose_name='轮播商品排序')),
            ],
            options={
                'verbose_name': '首页轮播商品',
                'verbose_name_plural': '首页轮播商品',
            },
        ),
        migrations.CreateModel(
            name='shop_album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('image_address', models.ImageField(upload_to='shop_album/%Y%m%d', verbose_name='图片地址')),
            ],
            options={
                'verbose_name': '商品相册',
                'verbose_name_plural': '商品相册',
            },
        ),
        migrations.CreateModel(
            name='shop_SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('sku_name', models.CharField(max_length=50, verbose_name='商品SKU名')),
                ('sku_introduction', models.CharField(blank=True, max_length=255, null=True, verbose_name='商品SKU简介')),
                ('sku_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='商品SKU价格')),
                ('sku_stock', models.IntegerField(default=0, verbose_name='商品SKU库存')),
                ('sku_sale', models.IntegerField(default=0, verbose_name='商品SKU销量')),
                ('sku_address', models.ImageField(upload_to='shop_SKU/%Y%m%d', verbose_name='商品LOGO地址')),
                ('is_shelf', models.BooleanField(choices=[(1, '上架'), (0, '未上架')], default=False, verbose_name='商品SKU是否上架')),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
            },
        ),
        migrations.CreateModel(
            name='shop_sort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('sort_name', models.CharField(max_length=50, verbose_name='商品分类名')),
                ('sort_introduction', models.CharField(blank=True, max_length=50, null=True, verbose_name='商品分类简介')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
            },
        ),
        migrations.CreateModel(
            name='shop_SPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('spu_name', models.CharField(max_length=50, verbose_name='商品SPU名称')),
                ('spu_content', models.CharField(blank=True, max_length=255, null=True, verbose_name='商品SPU详情')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
            },
        ),
        migrations.CreateModel(
            name='unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('unit_name', models.CharField(max_length=20, verbose_name='单位名')),
            ],
            options={
                'verbose_name': '商品单位表',
                'verbose_name_plural': '商品单位表',
            },
        ),
        migrations.AddField(
            model_name='shop_sku',
            name='sort_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop_sort', verbose_name='商品分类id'),
        ),
        migrations.AddField(
            model_name='shop_sku',
            name='spu_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop_SPU', verbose_name='商品SPUid'),
        ),
        migrations.AddField(
            model_name='shop_album',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop_SKU', verbose_name='商品SKUID'),
        ),
        migrations.AddField(
            model_name='lunbo',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop_SKU', verbose_name='商品SKUID'),
        ),
        migrations.AddField(
            model_name='active_sku',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop_SKU', verbose_name='商品SKUID'),
        ),
        migrations.AddField(
            model_name='active_sku',
            name='zone_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.active_zone', verbose_name='专区ID'),
        ),
    ]
