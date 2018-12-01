from django.db import models

from db.base_model import BaseModel


class Transport(BaseModel):
    """运输方式"""
    tran_name = models.CharField(max_length=50, verbose_name="运输名字")
    tran_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="运费")

    def __str__(self):
        return self.tran_name

    class Meta:
        db_table = "transport"
        verbose_name = "运输方式管理"
        verbose_name_plural = verbose_name


class PayMethod(BaseModel):
    """支付方式"""
    name = models.CharField(max_length=50, verbose_name="支付形式")
    logo = models.ImageField(db_column="pay/%Y", verbose_name="logo")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pay_method"
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name


class Order(BaseModel):
    """订单信息表"""
    order_status = (
        (0, "待付款"),
        (1, "待发货"),
        (2, "已发货"),
        (3, "完成"),
        (4, "已评价"),
        (5, "申请退款"),
        (6, "已退款"),
        (7, "取消订单"),
    )
    order_sn = models.CharField(max_length=64, verbose_name="订单编号",unique=True)
    order_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="商品总金额")
    user = models.ForeignKey(to="user.User", verbose_name="用户id")
    username = models.CharField(max_length=50, verbose_name="收货人姓名")
    telephone = models.CharField(max_length=11, verbose_name="收货人电话")
    address = models.CharField(max_length=255, verbose_name="收货人地址")
    status = models.IntegerField(choices=order_status, verbose_name="订单状态", default=0)
    transport = models.CharField(max_length=50, verbose_name="运输方式")
    transport_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="运费")
    pay_method = models.ForeignKey(to="PayMethod", verbose_name="支付方式", null=True, blank=True)
    order_money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="实付总金额")

    def __str__(self):
        return self.order_sn

    class Meta:
        db_table = 'order'
        verbose_name = "订单信息管理"
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    order = models.ForeignKey(to="Order", verbose_name='订单id')
    goods_sku = models.ForeignKey(to="shop.Shop_SKU", verbose_name="订单商品SKUID")
    count = models.IntegerField(verbose_name="订单商品数量")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="订单商品价格")

    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品管理'
        verbose_name_plural = verbose_name
