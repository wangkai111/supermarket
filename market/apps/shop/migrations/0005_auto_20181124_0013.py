# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-24 00:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20181124_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop_sku',
            old_name='unit_id',
            new_name='unit',
        ),
        migrations.AlterField(
            model_name='active_sku',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop_SKU', verbose_name='商品SKUID'),
        ),
        migrations.AlterField(
            model_name='active_sku',
            name='zone_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Active_zone', verbose_name='专区ID'),
        ),
        migrations.AlterField(
            model_name='lunbo',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop_SKU', verbose_name='商品SKUID'),
        ),
        migrations.AlterField(
            model_name='shop_album',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop_SKU', verbose_name='商品SKUID'),
        ),
        migrations.AlterField(
            model_name='shop_sku',
            name='sort_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop_sort', verbose_name='商品分类id'),
        ),
        migrations.AlterField(
            model_name='shop_sku',
            name='spu_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop_SPU', verbose_name='商品SPUid'),
        ),
        migrations.AlterField(
            model_name='shop_sku',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Unit', verbose_name='单位'),
        ),
    ]
