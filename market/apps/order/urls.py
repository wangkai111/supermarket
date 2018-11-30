from django.conf.urls import url

from order.views import TrueOrder, Order

urlpatterns = [
    url(r'^TrueOrder/$',TrueOrder.as_view(),name="确认订单"),
    url(r'^Order/$',Order.as_view(),name="确认支付"),
]