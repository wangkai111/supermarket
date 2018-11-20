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


# 设置注册表单
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
