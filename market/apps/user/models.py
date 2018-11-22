from django.db import models

from db.base_model import BaseModel


# 设置用户模型数据
class User(BaseModel):
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

    class Meta:
        db_table = 'user'
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.telephone
