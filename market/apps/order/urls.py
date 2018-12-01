from django.conf.urls import url

from order.views import TrueOrder, OrderShow, pay, success

urlpatterns = [
    url(r'^TrueOrder/$',TrueOrder.as_view(),name="确认订单"),
    url(r'^OrderShow/$',OrderShow.as_view(),name="确认支付"),
    url(r'^pay/$',pay,name="发起支付"),
    url(r'^success/$',success,name="支付成功"),
]