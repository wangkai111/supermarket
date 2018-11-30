from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models

from db.base_model import BaseModel


class Shop_sort(BaseModel):
    """商品分类"""
    sort_name = models.CharField(max_length=50, verbose_name="商品分类名")
    sort_introduction = models.CharField(max_length=50, null=True, blank=True, verbose_name="商品分类简介")

    def __str__(self):
        return self.sort_name

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name


class Shop_SPU(BaseModel):
    """商品SPU表"""
    spu_name = models.CharField(max_length=50, verbose_name="商品SPU名称")
    # 使用富文本编辑器渲染之前的普通文本框
    spu_content = RichTextUploadingField(verbose_name="商品SPU详情")
    # spu_content = models.TextField(verbose_name="商品SPU详情")

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name


class Unit(BaseModel):
    """商品单位表"""
    unit_name = models.CharField(max_length=20, verbose_name="单位名")

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "商品单位表"
        verbose_name_plural = verbose_name


class Shop_SKU(BaseModel):
    """商品SKU表"""
    is_shelf_choices = (
        (1, "上架"),
        (0, "未上架")
    )
    sku_name = models.CharField(max_length=50, verbose_name="商品SKU名")
    sku_introduction = models.CharField(max_length=255, null=True, blank=True, verbose_name="商品SKU简介")
    sku_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="商品SKU价格")
    unit = models.ForeignKey(to="Unit", verbose_name="单位")
    sku_stock = models.IntegerField(default=0, verbose_name="商品SKU库存")
    sku_sale = models.IntegerField(default=0, verbose_name="商品SKU销量")
    sku_address = models.ImageField(upload_to="shop_SKU/%Y%m/%d", verbose_name="商品LOGO地址")
    is_shelf = models.BooleanField(default=0, choices=is_shelf_choices, verbose_name="商品SKU是否上架")
    sort_id = models.ForeignKey(to="Shop_sort", verbose_name="商品分类id")
    spu_id = models.ForeignKey(to="Shop_SPU", verbose_name="商品SPUid")

    # 自定义字段
    def sku_logo(self):
        return "<img style='width:60px' src='{}{}'/>".format(settings.MEDIA_URL,self.sku_address)

    sku_logo.allow_tags = True
    sku_logo.short_description = "LOGO"

    def __str__(self):
        return self.sku_name

    class Meta:
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name


class Shop_album(BaseModel):
    """商品相册"""
    image_address = models.ImageField(upload_to="shop_album/%Y%m/%d", verbose_name="图片地址")
    sku_id = models.ForeignKey(to="Shop_SKU", verbose_name="商品SKUID")

    class Meta:
        verbose_name = "商品相册"
        verbose_name_plural = verbose_name


class Lunbo(BaseModel):
    """首页轮播商品"""
    lunbo_name = models.CharField(max_length=50, verbose_name="轮播名称")
    image_address = models.ImageField(upload_to="shop_lunbo/%Y%m/%d", verbose_name="图片地址")
    order = models.IntegerField(default=0, verbose_name="轮播商品排序")
    sku_id = models.ForeignKey(to="Shop_SKU", verbose_name="商品SKUID")

    # 自定义字段
    def lun_image(self):
        return "<img style='width:60px' src='{}{}'/>".format(settings.MEDIA_URL,self.image_address)

    lun_image.allow_tags = True
    lun_image.short_description = "轮播图片"

    def __str__(self):
        return self.lunbo_name

    class Meta:
        verbose_name = "首页轮播商品"
        verbose_name_plural = verbose_name


class Active(BaseModel):
    """首页活动表"""
    active_name = models.CharField(max_length=50, verbose_name="活动名称")
    image_address = models.ImageField(upload_to="shop_active/%Y%m/%d", verbose_name="图片地址")
    url_address = models.URLField(null=True, verbose_name="活动地址")

    def __str__(self):
        return self.active_name

    class Meta:
        verbose_name = "首页活动表"
        verbose_name_plural = verbose_name


class Active_zone(BaseModel):
    """首页活动专区"""
    is_shelf_choices = (
        (1, "上架"),
        (0, "未上架")
    )
    zone_name = models.CharField(max_length=50, verbose_name="活动专区名称")
    zone_content = models.CharField(max_length=255, null=True, blank=True, verbose_name="活动专区描述")
    zone_order = models.IntegerField(default=0, verbose_name="活动专区排序")
    is_shelf = models.BooleanField(choices=is_shelf_choices, default=0, verbose_name="活动专区是否上架")

    def __str__(self):
        return self.zone_name

    class Meta:
        verbose_name = "首页活动专区"
        verbose_name_plural = verbose_name


class Active_SKU(BaseModel):
    """首页专区活动商品表"""
    zone_id = models.ForeignKey(to="Active_zone", verbose_name="专区ID")
    sku_id = models.ForeignKey(to="Shop_SKU", verbose_name="商品SKUID")

    class Meta:
        verbose_name = "首页专区活动商品表"
        verbose_name_plural = verbose_name
