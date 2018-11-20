from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")  # 设置用户注册时间
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")  # 设置用户修改信息时间
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")  # 设置是否假删除

    class Meta:
        # 说明是一个抽象的模型类,不会被迁移
        abstract = True
