from django.conf.urls import url

from user.views import login, reg, forgetpassword, MemberView, InforView, verification_code

urlpatterns = [
    url(r'^$', login, name="登录"),
    url(r'^reg/$', reg, name="注册"),
    url(r'^forgetpassword/$', forgetpassword, name="忘记密码"),
    url(r'^member/$', MemberView.as_view(), name="个人中心"),
    url(r'^infor/$', InforView.as_view(), name="个人资料"),
    url(r'^verification_code/$',verification_code, name="获取验证码"),
]
