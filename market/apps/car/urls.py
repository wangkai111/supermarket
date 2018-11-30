from django.conf.urls import url

from car.views import AddShopCart, ShopCart

urlpatterns = [
    url(r'^AddShopCart/$',AddShopCart.as_view(),name="添加购物车"),
    url(r'^$',ShopCart.as_view(),name="购物车界面"),
]