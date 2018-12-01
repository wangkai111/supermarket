import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
import re
import random
from db.base_view import BaseView
from user.forms import RegForm, InforForm, ForgetForm, AddressModelForm, AddressUpdateModelForm
from user.help import set_password, send_sms
from user.models import User, Address
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
                # 保存id,头像登录标识符到session
                request.session["id"] = user.id
                request.session["telephone"] = user.telephone
                # 判断链接上是否有参数next,如果有就跳转到指定页面
                # 跳转到主页
                next = request.GET.get("next")
                if next:
                    return redirect(next)
                else:
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
    if request.method == "POST":
        # 接收数据
        res = request.POST
        # 创建form对象,验证form表单中的数据是否写好
        form = ForgetForm(res)
        # 验证是否合法
        if form.is_valid():
            # 获取清洗后的数据
            aa = form.cleaned_data
            # 得到表单中的手机号
            telephone = aa.get("telephone")
            # 通过手机号获取到数据库中的这条数据
            user = User.objects.filter(telephone=telephone).first()
            # 判断手机号是否已经存在数据库中
            if user:
                # 获取表单中的密码
                password = aa.get("password")
                # 加密密码成哈希
                mpassword = set_password(password)
                # 将加密后的密码更新到数据库中
                User.objects.filter(telephone=telephone).update(password=mpassword)
                return redirect("user:登录")
            else:
                context = {
                    "a": "该手机号之前未注册过"
                }
                return render(request, "user/forgetpassword.html", context)
        else:
            # 错误,将错误信息显示到页面
            context = {
                "errors": form.errors
            }
            return render(request, "user/forgetpassword.html", context)
    else:
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
            # 连接到redis中.
            r = get_redis_connection("default")
            # 将电话号码和随机码以键和值的形式存到redis中
            r.set(telephone, random_code)
            # 设置过期时间
            r.expire(telephone, 120)
            # 成功,让阿里发送短信提示
            # __business_id = uuid.uuid1()
            # # 信息
            # params = "{\"code\":\"%s\",\"product\":\"kkw的电商超市\"}" % random_code
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
        context = {
            "telephone": request.session.get("telephone"),
            "logo": request.session.get("logo")
        }
        return render(request, 'user/member.html', context)

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
        # 头像单独获取
        tou = request.FILES
        # 获取表单中的数据
        data = request.POST
        # 处理数据
        form = InforForm(data, tou)
        # 验证是否合法
        if form.is_valid():
            # 开始验证
            # 获取清洗后的数据
            a = form.cleaned_data
            # 通过session获取得到id
            id = request.session["id"]
            # 将数据更新到数据库
            user = User.objects.filter(pk=id).first()
            user.name = a.get("name")
            user.sex = a.get("sex")
            user.birthday = a.get("birthday")
            user.school_name = a.get("school_name")
            user.address = a.get("address")
            user.hometown = a.get("hometown")
            user.logo = a.get("logo")
            request.session["logo"] = user.logo
            user.save()
            # 跳转到个人中心
            return redirect("user:个人中心")
        else:
            # 抛出错误信息
            context = {
                "errors": form.errors,
            }
            return render(request, 'user/infor.html', context)


class AddressShow(BaseView):
    """管理收货地址"""

    def get(self, request):
        # 获取id
        id = request.session.get("id")
        # 获取该id下的用户收货地址数据
        addresses = Address.objects.filter(userid_id=id, isDelete=False).order_by("-isDefault")
        # 回显数据
        context = {
            "addresses": addresses,
        }
        return render(request, "user/gladdress.html", context)

    def post(self, request):
        pass


class AddressAdd(BaseView):
    """新增收货地址"""

    def get(self, request):
        return render(request, "user/address.html")

    def post(self, request):
        # 获取到用户id
        id = request.session.get("id")
        # 接收参数
        data = request.POST.dict()
        data["userid_id"] = id
        # 验证参数
        form = AddressModelForm(data)
        # 处理数据
        if form.is_valid():
            """
            # 清洗后的数据
            cleaned_data = form.cleaned_data
            第一种方式,原生
            # 将用户id添加到清洗后的数据里
            cleaned_data["userid_id"] = id
            # 将清洗后的数据保存到数据库中
            Address.objects.create(**cleaned_data)
            """
            # 第二种方式,自定义在对象上添加键和值
            form.instance.userid_id = id
            # modelform对象上有个save()方法,直接就能保存数据
            form.save()
            # 跳转到收货地址
            return redirect("user:管理收货地址")

        else:
            # 抛出错误信息
            context = {
                "form": form,
            }
            # 返回响应
            return render(request, "user/address.html", context)


class AddressUpdate(BaseView):
    """修改收货地址"""

    def get(self, request, id):
        # 获取用户id
        user_id = request.session.get("id")
        try:
            # 获取该id用户下的地址
            address = Address.objects.get(userid_id=user_id, pk=id)
        except Address.DoesNotExist:
            return redirect("user:管理收货地址")
        # 渲染页面
        context = {
            "address": address,
        }
        return render(request, "user/addressupdate.html", context)

    def post(self, request, id):
        # 接收数据
        data = request.POST.dict()
        # 获取用户id
        user_id = request.session.get("id")
        # 将用户id保存到data中
        data['userid_id'] = user_id
        # 验证数据
        form = AddressUpdateModelForm(data)
        # 处理数据
        if form.is_valid():
            # 返回清洗后的数据
            cleande_data = form.cleaned_data
            # 将返回后的数据更新到数据库中
            Address.objects.filter(pk=id, userid_id=user_id).update(**cleande_data)
            # 响应
            return redirect("user:管理收货地址")
        else:
            context = {
                "form": form,
                "address": data,
            }
            return render(request, "user/addressupdate.html", context)


def del_address(request):
    """删除收货地址"""
    # 必须登录,才能获取到用户id
    if request.method == "POST":
        user_id = request.session.get("id")
        id = request.POST.get("id")
        if user_id is None:
            return JsonResponse({"val": 1, "err": "没有登录!"})
        else:
            # 删除使用假删除更好
            Address.objects.filter(userid_id=user_id, pk=id).update(isDelete=True)
            return JsonResponse({"val": 0, "err": "删除成功"})
    else:
        return JsonResponse({"var": 2, "err": "请求方式错误"})
