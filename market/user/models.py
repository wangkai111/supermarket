from django.db import models


class User(models.Model):
    password = models.CharField(max_length=32)  # 设置密码
    telephone = models.CharField(max_length=11)  # 设置用户名
    create_time = models.DateField(auto_now_add=True)  # 设置用户注册时间
    update_time = models.DateField(auto_now=True)  # 设置用户修改信息时间

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.telephone


# class Person(models.Model):
#     sex_choices = (
#         (1, "男"),
#         (2, "女"),
#         (3, "保密"),
#     )
#     name = models.CharField(max_length=10, default="")  # 设置用户名昵称
#     sex = models.SmallIntegerField(choices=sex_choices, default=3)  # 设置性别
#     isDelete = models.BooleanField(default=False)  # 设置是否假删除
#     birthday = models.DateField(null=True)  # 设置生日
#     create_time = models.DateTimeField(auto_now_add=True)  # 设置用户注册时间
#     update_time = models.DateTimeField(auto_now=True)  # 设置用户修改信息时间
#     school_name = models.CharField(max_length=25, null=True)  # 设置用户学校名字
#     address = models.CharField(max_length=50, null=True)  # 设置用户地址
