from django.conf.urls import url

from user.views import login, reg, forgetpassword, MemberView, InforView, verification_code, AddressShow, AddressAdd, \
    AddressUpdate, del_address

urlpatterns = [
    url(r'^$', login, name="登录"),
    url(r'^reg/$', reg, name="注册"),
    url(r'^forgetpassword/$', forgetpassword, name="忘记密码"),
    url(r'^member/$', MemberView.as_view(), name="个人中心"),
    url(r'^infor/$', InforView.as_view(), name="个人资料"),
    url(r'^verification_code/$',verification_code, name="获取验证码"),
    url(r'^AddressShow/$',AddressShow.as_view(), name="管理收货地址"),
    url(r'^AddressAdd/$',AddressAdd.as_view(), name="新增收货地址"),
    url(r'^AddressUpdate/(?P<id>\d+)/$',AddressUpdate.as_view(), name="修改收货地址"),
    url(r'^del_address/$',del_address, name="删除收货地址"),
]
