from django.conf.urls import url

from shop.views import shop_index

urlpatterns = [
    url(r'^$',shop_index,name='商城主页')
]