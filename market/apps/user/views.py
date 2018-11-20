from django.shortcuts import render, redirect
from django.views import View

from user.forms import RegForm
from user.help import set_password
from user.models import User


def login(request):  # 登录界面
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
                # 保存登录标识符到session
                request.session["telephone"] = telephone
                # 跳转到主页
                return redirect("shop:商城主页")
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


def reg(request):  # 注册界面
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


def forgetpassword(request):  # 忘记密码界面
    return render(request, "user/forgetpassword.html")


class MemberView(View):
    def get(self, request):
        return render(request, 'user/member.html')

    def post(self, request):
        pass
