from django.db import models

from db.base_model import BaseModel


class shop_lunbo(BaseModel):
    """首页轮播商品"""
    lunbo_name = models.CharField(max_length=0,null=True,verbose_name="名称")
    lunbo_pir = models.ImageField(upload_to="shop_head/%Y%m%d",default="images/banner.png",verbose_name="轮播图片")
    lunbo_SKUID = models.

