from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

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
from user.models import User, Address


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
    sr_yzm = forms.CharField(max_length=4,
                             error_messages={
                                 "required": "验证码不能为空",
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

    # 单独验证验证码
    def clean_sr_yzm(self):
        res = self.cleaned_data
        telephone = res.get("telephone")
        sr_yzm = res.get("sr_yzm")
        # 连接redis数据库
        r = get_redis_connection("default")
        # 获取redis中的验证码
        random_code = r.get(telephone)
        # 判断数据库中的验证码和用户提交的验证码是否一致
        if random_code is None:
            raise forms.ValidationError("验证码已经过期或者错误")
        else:
            # 需要解码
            random_code = random_code.decode("utf-8")
            # 判断
            if telephone:
                if random_code != sr_yzm:
                    raise forms.ValidationError("验证码错误!")
                return sr_yzm
            else:
                return sr_yzm


# 验证忘记密码
class ForgetForm(forms.Form):
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
    sr_yzm = forms.CharField(max_length=4,
                             error_messages={
                                 "required": "验证码不能为空",
                             },
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

    # 单独验证验证码
    def clean_sr_yzm(self):
        res = self.cleaned_data
        telephone = res.get("telephone")
        sr_yzm = res.get("sr_yzm")
        # 连接redis数据库
        r = get_redis_connection("default")
        # 判断
        if telephone:
            # 获取redis中的验证码
            random_code = r.get(telephone)
            if random_code is None:
                raise forms.ValidationError("验证码已经过期或者错误")
            else:
                # 需要解码
                random_code = random_code.decode("utf-8")
                # 判断数据库中的验证码和用户提交的验证码是否一致
                if random_code != sr_yzm:
                    raise forms.ValidationError("验证码错误!")
                return sr_yzm
        else:
            return sr_yzm


# 验证个人中心
class InforForm(forms.Form):
    name = forms.CharField(error_messages={"required": "请填写昵称"})
    sex = forms.IntegerField()
    birthday = forms.DateField(error_messages={"required": "请填写生日"})
    school_name = forms.CharField(error_messages={"required": "请填写学校名字"})
    address = forms.CharField(error_messages={"required": "请填写详细地址"})
    hometown = forms.CharField(error_messages={"required": "请填写家乡地址"})
    logo = forms.FileField()


# 验证新增收货地址
class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['hcity', 'hproper', 'harea', 'username', 'telephone', 'isDefault', 'detail']

        error_messages = {
            "harea": {
                "required": "收货地址必填"
            },
            "username": {
                "required": "收货人姓名必填"
            },
            "telephone": {
                "required": "收货人手机号必填"
            },
            "detail": {
                "required": "详细地址必填"
            },
        }

    # 验证当前用户的收货地址数量,不能超过6个
    def clean(self):
        # 得到数据
        userid_id = self.data.get("userid_id")
        count = Address.objects.filter(userid_id=userid_id,isDelete=False).count()
        if count >= 6:
            raise forms.ValidationError("收货地址不能超过6个")

        # 默认收货地址只有一个,判断当前添加的是 isDefault==True
        isDefault = self.cleaned_data.get("isDefault")
        if isDefault:
            # 其它的地址就设置成False
            Address.objects.filter(userid_id=userid_id).update(isDefault=False)
        return self.cleaned_data


# 验证修改收货地址
class AddressUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['hcity', 'hproper', 'harea', 'username', 'telephone', 'isDefault', 'detail']

        error_messages = {
            "harea": {
                "required": "收货地址必填"
            },
            "username": {
                "required": "收货人姓名必填"
            },
            "telephone": {
                "required": "收货人手机号必填"
            },
            "detail": {
                "required": "详细地址必填"
            },
        }

    # 验证当前用户的收货地址数量,不能超过6个
    def clean(self):
        # 得到数据
        userid_id = self.data.get("userid_id")

        # 默认收货地址只有一个,判断当前添加的是 isDefault==True
        isDefault = self.cleaned_data.get("isDefault")
        if isDefault:
            # 其它的地址就设置成False
            Address.objects.filter(userid_id=userid_id).update(isDefault=False)
        return self.cleaned_data
