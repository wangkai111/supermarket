from django.core.validators import RegexValidator
from django.db import models

from db.base_model import BaseModel


class User(BaseModel):
    """设置用户模型数据"""
    sex_choices = (
        (1, "男"),
        (2, "女"),
    )
    password = models.CharField(max_length=32, verbose_name="密码")  # 设置密码
    telephone = models.CharField(max_length=11, verbose_name="手机号")  # 设置用户名
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="用户名")  # 设置用户名昵称
    sex = models.SmallIntegerField(choices=sex_choices, default=1, verbose_name="性别")  # 设置性别
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")  # 设置生日
    school_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="学校名字")  # 设置用户学校名字
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="位置")  # 设置用户地址
    hometown = models.CharField(max_length=50, null=True, blank=True, verbose_name="家乡")  # 设置家乡
    # 设置头像
    logo = models.ImageField(upload_to="head/%Y%m/%d", default="head/memtx.png", verbose_name="用户头像")

    class Meta:
        db_table = 'user'
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.telephone


class Address(BaseModel):
    """设置收货地址模型"""
    hcity = models.CharField(max_length=50, verbose_name="省")
    hproper = models.CharField(max_length=50, verbose_name="市")
    harea = models.CharField(max_length=50, verbose_name="区")
    detail = models.CharField(max_length=255, verbose_name="详细地址")
    username = models.CharField(max_length=50, verbose_name="收货人姓名")
    telephone = models.CharField(max_length=11,
                                 verbose_name="收货人手机号",
                                 validators=[
                                     RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')
                                 ],
                                 )
    userid = models.ForeignKey(to="user.User", verbose_name="用户id", related_name="userid")
    isDefault = models.BooleanField(default=False, verbose_name="是否为默认地址")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'address'
        verbose_name = "用户地址管理"
        verbose_name_plural = verbose_name
