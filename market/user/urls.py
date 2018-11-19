from django.conf.urls import url

from user.views import login, reg, forgetpassword

urlpatterns = [
    url(r'^$',login,name="登录"),
    url(r'^reg/$', reg, name="注册"),
    url(r'^forgetpassword/$',forgetpassword,name="忘记密码"),
]