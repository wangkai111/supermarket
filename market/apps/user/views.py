import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
import re
import random
from db.base_view import BaseView
from user.forms import RegForm, InforForm
from user.help import set_password, send_sms
from user.models import User
from django_redis import get_redis_connection


def login(request):
    """登录界面"""
    if request.method == "POST":
        # 获取表单中的手机号和密码
        telephone = request.POST.get("telephone")
        password = request.POST.get("password")

        # 通过表单中的手机号获取数据库中的手机号
        # 首先获取的是一条集合,再通过集合.first()  可得到里面一条对象
        user = User.objects.filter(telephone=telephone).first()
        # 验证
        # 判断表单手机号是否在数据库中
        if user:
            # 获取数据库密码(对象.属性名)
            user_password = user.password

            # form表单中获取的密码加密
            password = set_password(password)

            # 验证表单的密码是否和数据库的密码一致
            if user_password == password:
                # 保存id登录标识符到session
                request.session["id"] = user.id
                # 跳转到主页
                return redirect("user:个人中心")
            else:
                context = {
                    "a": "用户名或者密码错误"
                }
                return render(request, "user/login.html", context)
        else:
            context = {
                "a": "请输入用户名和密码"
            }
            return render(request, "user/login.html", context)
    else:
        return render(request, "user/login.html")


def reg(request):
    """注册界面"""
    if request.method == "POST":
        # 接收数据
        res = request.POST
        # 判断用户是否勾选用户协议
        if res.get("checkbox"):
            # 判断手机号是否已经存在数据库中
            if User.objects.filter(telephone=res.get("telephone")):
                context = {
                    "a": "手机号已经被注册"
                }
                return render(request, "user/reg.html", context)
            else:
                # 创建form对象,验证form表单中的数据是否写好
                form = RegForm(res)
                # 判断是否合法性
                if form.is_valid():
                    # 开始验证
                    # 处理数据,将清洗后数据保存到数据库
                    aa = form.cleaned_data
                    # 获取表单密码
                    password = aa.get("password")
                    # 密码加密成哈希
                    password = set_password(password)
                    # 将手机号和加密后的密码创建到数据库
                    User.objects.create(telephone=aa.get("telephone"), password=password)
                    # 跳转到登录界面
                    return redirect('user:登录')
                else:
                    # 错误,将错误信息显示到页面
                    context = {
                        "errors": form.errors,
                        "res": res
                    }
                    return render(request, "user/reg.html", context)
        else:
            context = {
                "c": "请同意用户协议"
            }
            return render(request, "user/reg.html", context)

    else:
        return render(request, "user/reg.html")


def forgetpassword(request):
    """忘记密码界面"""
    return render(request, "user/forgetpassword.html")


def verification_code(request):
    """短信验证,获取验证码"""
    if request.method == "POST":
        # 获取手机号
        telephone = request.POST.get("telephone")
        # 创建正则对象
        r_telephone = re.compile('^1[3-9]\d{9}$')
        # 匹配表单中传入的手机号
        res = re.search(r_telephone, telephone)
        if res:
            # 创建随机码
            random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
            # print(random_code)
            # 连接到redis中
            r = get_redis_connection("default")
            # 将电话号码和随机码以键和值的形式存到redis中
            r.set(telephone, random_code)
            # 设置过期时间
            r.expire(telephone, 120)
            # 成功,让阿里发送短信提示
            # __business_id = uuid.uuid1()
            # # 信息
            # params = "{\"code\":\"%s\",\"product\":\"王凯专属服务\"}" % random_code
            # send_sms(__business_id, telephone, "注册验证", "SMS_2245271", params)

            return JsonResponse({"ok": 0})
        else:
            return JsonResponse({"err": 0, "errmsg": "手机号码格式错误"})
    else:
        # 提示请求方式错误,是json对象
        return JsonResponse({"err": 1, "errmsg": "短信验证码发送失败"})


class MemberView(BaseView):
    """个人中心"""

    def get(self, request):
        return render(request, 'user/member.html')

    def post(self, request):
        pass


class InforView(BaseView):
    """个人资料"""

    def get(self, request):
        # 通过session获取id
        id = request.session["id"]
        # 通过id获取该条id所对应的信息
        data = User.objects.get(pk=id)
        # 将数据响应到html中
        context = {
            "data": data
        }
        return render(request, 'user/infor.html', context)

    def post(self, request):
        # 得到参数
        # 获取表单中的数据
        data = request.POST
        # 处理数据
        form = InforForm(data)
        # 验证是否合法
        if form.is_valid():
            # 开始验证
            # 获取清洗后的数据
            a = form.cleaned_data
            # 通过session获取得到id
            id = request.session["id"]
            # 将数据更新到数据库
            User.objects.filter(pk=id).update(name=a.get("name"),
                                              sex=a.get("sex"),
                                              birthday=a.get("birthday"),
                                              school_name=a.get("school_name"),
                                              address=a.get("address"),
                                              hometown=a.get("hometown"),
                                              )
            # 跳转到个人中心
            return redirect("user:个人中心")
        else:
            # 抛出错误信息
            context = {
                "errors": form.errors,
            }
            return render(request, 'user/infor.html', context)
