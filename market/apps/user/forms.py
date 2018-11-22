from django import forms
from django.core.validators import RegexValidator


# 设置登录表单
# class LoginForm(forms.Form):
#     telephone = forms.IntegerField(error_messages={
#         "required": "手机号不能为空"
#     },
#         validators=[
#             RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误")
#         ]
#     )
#     password = forms.CharField(max_length=32,
#                                error_messages={
#                                    "required": "密码不能为空"
#                                },
#                                validators=[
#                                    RegexValidator(r'^\d{6}$', "密码格式错误")
#                                ],
#                                )


# 验证注册表单
class RegForm(forms.Form):
    telephone = forms.CharField(error_messages={
        "required": "手机号不能为空"
    },
        validators=[
            RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误")
        ],
    )
    password = forms.CharField(max_length=32,
                               error_messages={
                                   "required": "密码不能为空",
                               },
                               validators=[
                                   RegexValidator(r'^\d{6}$', "密码必须是6位数字")
                               ],
                               )
    rpassword = forms.CharField(max_length=32,
                                error_messages={
                                    "required": "密码不能为空",
                                },
                                validators=[
                                    RegexValidator(r'^\d{6}$', "密码必须是6位数字")
                                ],
                                )
    yzm = forms.CharField(max_length=4,
                          error_messages={
                              "required":"验证码不能为空",
                          }
                          )

    def clean(self):
        # 综合校验
        # 得到数据
        data = self.cleaned_data
        password = data.get("password")
        rpassword = data.get("rpassword")
        # 判断两次密码是否一致
        if password != rpassword:
            # 不一致,抛出错误信息
            raise forms.ValidationError({"rpassword": "两次密码不一致"})
        # 验证成功,得到全部清洗后的数据
        return data

    # def clean_yzm(self):
    #     # 验证获取到的验证码和表单提交的是否一致
    #     data = self.cleaned_data
    #     yzm = data.get("yzm")
    #     random_code =


# 验证个人中心
class InforForm(forms.Form):
    name = forms.CharField(error_messages={"required": "请填写昵称"})
    sex = forms.IntegerField()
    birthday = forms.DateField(error_messages={"required": "请填写生日"})
    school_name = forms.CharField(error_messages={"required": "请填写学校名字"})
    address = forms.CharField(error_messages={"required":"请填写详细地址"})
    hometown = forms.CharField(error_messages={"required":"请填写家乡地址"})